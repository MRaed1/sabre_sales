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

        start = frappe.db.sql("""
            SELECT IFNULL(MAX(CAST(SUBSTRING(name, 6) AS UNSIGNED)), 0)
            FROM `tabMIDT Record` WHERE name LIKE 'MIDT-%'
        """)[0][0]

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

        month_list = ', '.join(sorted(months))
        upload.db_set('status', 'Imported')
        upload.db_set('records_imported', len(values))
        upload.db_set('import_log', 'Imported ' + str(len(values)) + ' rows for months: ' + month_list)
        frappe.db.commit()

        return {'ok': True, 'records': len(values), 'months': sorted(months)}

    except Exception as e:
        frappe.db.rollback()
        upload.db_set('status', 'Failed')
        upload.db_set('import_log', str(e)[:500])
        frappe.db.commit()
        raise
