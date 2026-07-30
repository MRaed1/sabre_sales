import frappe
import openpyxl
from frappe.utils import now


@frappe.whitelist()
def import_midt(upload_name):
    """Parse the Excel attached to a MIDT Upload doc and load it into MIDT Record.
    Replaces overlapping months so monthly re-uploads are safe."""
    upload = frappe.get_doc('MIDT Upload', upload_name)

    if not upload.midt_file:
        frappe.throw('Please attach the MIDT Excel file first.')

    allowed = ['System Manager', 'Sabre Head Of Sales', 'Sabre Account Manager']
    user_roles = frappe.get_roles(frappe.session.user)
    if not any(r in user_roles for r in allowed):
        frappe.throw('You are not allowed to import MIDT data.')

    file_doc = frappe.get_doc('File', {'file_url': upload.midt_file})
    path = file_doc.get_full_path()

    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        if 'Sheet1' in wb.sheetnames:
            ws = wb['Sheet1']
        else:
            ws = max(wb.worksheets, key=lambda s: s.max_row)

        rows = ws.iter_rows(values_only=True)
        header = next(rows)

        data = []
        months = set()
        for r in rows:
            if not r or not r[0] or str(r[0]) == 'Overall':
                continue
            month = r[0].date() if hasattr(r[0], 'date') else r[0]
            months.add(str(month))
            data.append((month, r[2], r[3], r[4], r[6], r[7], r[8],
                         int(r[9] or 0), int(r[10] or 0), int(r[11] or 0), int(r[15] or 0)))

        if not data:
            frappe.throw('No data rows found in the file. Is this the correct MIDT export?')

        for m in months:
            frappe.db.sql("DELETE FROM `tabMIDT Record` WHERE month = %s", m)

        start = int(frappe.db.sql("""
            SELECT IFNULL(MAX(CAST(SUBSTRING(name, 6) AS UNSIGNED)), 0)
            FROM `tabMIDT Record` WHERE name LIKE 'MIDT-%'
        """)[0][0])

        ts = now()
        user = frappe.session.user
        fields = ['name', 'owner', 'creation', 'modified', 'modified_by', 'docstatus', 'idx',
                  'month', 'sc_code', 'sc_code_name', 'pcc', 'iata', 'iata_name', 'supplier',
                  'sabre_bookings', 'amadeus_bookings', 'travelport_bookings', 'total_bookings']
        values = []
        for i, d in enumerate(data):
            name = 'MIDT-' + str(start + i + 1).zfill(7)
            values.append((name, user, ts, ts, user, 0, 0) + d)

        chunk = 5000
        total_chunks = (len(values) + chunk - 1) // chunk
        for ci in range(total_chunks):
            frappe.db.bulk_insert('MIDT Record', fields,
                                  values[ci * chunk:(ci + 1) * chunk], chunk_size=chunk)
            frappe.publish_progress(
                (ci + 1) * 100.0 / total_chunks,
                title='Importing MIDT data',
                description=str(min((ci + 1) * chunk, len(values))) + ' of ' + str(len(values)) + ' records'
            )

        new_agencies = _sync_agencies()

        month_list = ', '.join(sorted(months))
        frappe.db.set_value('MIDT Upload', upload_name, {
            'status': 'Imported',
            'records_imported': len(values),
            'import_log': 'Imported ' + str(len(values)) + ' rows for months: ' +
                          month_list + ' | New agencies created: ' + str(new_agencies),
        }, update_modified=False)
        frappe.db.commit()

        return {'ok': True, 'records': len(values), 'months': sorted(months),
                'new_agencies': new_agencies}

    except Exception as e:
        frappe.db.rollback()
        frappe.db.set_value('MIDT Upload', upload_name, {
            'status': 'Failed',
            'import_log': str(e)[:500],
        }, update_modified=False)
        frappe.db.commit()
        raise


def _sync_agencies():
    """Create Sabre Agency records for any IATA present in MIDT but not yet an agency.
    Runs after every import so new agencies appear automatically each month."""
    rows = frappe.db.sql("""
        SELECT iata,
               (SELECT r3.iata_name FROM `tabMIDT Record` r3
                WHERE r3.iata = r.iata AND r3.iata_name IS NOT NULL
                  AND r3.iata_name NOT IN ('-', 'Overall')
                GROUP BY r3.iata_name ORDER BY SUM(r3.total_bookings) DESC LIMIT 1) AS iata_name,
               (SELECT r2.pcc FROM `tabMIDT Record` r2
                WHERE r2.iata = r.iata
                GROUP BY r2.pcc ORDER BY SUM(r2.total_bookings) DESC LIMIT 1) AS main_pcc
        FROM `tabMIDT Record` r
        WHERE iata IS NOT NULL AND iata != ''
          AND iata_name IS NOT NULL AND iata_name NOT IN ('-', 'Overall')
        GROUP BY iata
    """, as_dict=True)

    existing = set(x[0] for x in frappe.db.sql("SELECT iata FROM `tabSabre Agency`"))
    used_names = set(x[0] for x in frappe.db.sql("SELECT name FROM `tabSabre Agency`"))

    ts = now()
    user = frappe.session.user
    fields = ['name', 'owner', 'creation', 'modified', 'modified_by', 'docstatus', 'idx',
              'agency_name', 'iata', 'pcc', 'current_gds']
    values = []
    for a in rows:
        if a.iata in existing:
            continue
        name = (a.iata_name or a.iata).strip()[:130]
        if name in used_names:
            name = name + ' - ' + a.iata
        used_names.add(name)
        values.append((name, user, ts, ts, user, 0, 0,
                       name, a.iata, a.main_pcc or '', ''))

    if values:
        frappe.db.bulk_insert('Sabre Agency', fields, values, chunk_size=1000)
    return len(values)
