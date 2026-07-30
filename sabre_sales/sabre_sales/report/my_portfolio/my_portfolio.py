import frappe


def execute(filters=None):
    filters = filters or {}
    user = frappe.session.user
    portfolio_status = filters.get('portfolio_status') or 'ALL'
    account_manager = filters.get('account_manager') or 'ALL'
    sabre_activity = filters.get('sabre_activity') or 'ALL'

    roles = frappe.get_roles(user)
    is_privileged = (
        user == 'Administrator'
        or 'Sabre Head Of Sales' in roles
        or 'System Manager' in roles
    )

    conditions = []
    values = {}

    if not is_privileged:
        conditions.append("a.account_manager = %(user)s")
        values['user'] = user

    if portfolio_status != 'ALL':
        conditions.append("a.portfolio_status = %(portfolio_status)s")
        values['portfolio_status'] = portfolio_status

    if account_manager != 'ALL':
        conditions.append("a.account_manager = %(account_manager)s")
        values['account_manager'] = account_manager

    where_clause = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    columns = [
        {'label': 'Agency', 'fieldname': 'agency', 'fieldtype': 'Link', 'options': 'Sabre Agency', 'width': 220},
        {'label': 'IATA', 'fieldname': 'iata', 'fieldtype': 'Data', 'width': 90},
        {'label': 'PCC', 'fieldname': 'pcc', 'fieldtype': 'Data', 'width': 80},
        {'label': 'Status', 'fieldname': 'status', 'fieldtype': 'Data', 'width': 150},
        {'label': 'Account Manager', 'fieldname': 'account_manager', 'fieldtype': 'Data', 'width': 180},
        {'label': 'Email', 'fieldname': 'email', 'fieldtype': 'Data', 'width': 180},
        {'label': 'Sabre Bookings', 'fieldname': 'sabre_bookings', 'fieldtype': 'Int', 'width': 110},
        {'label': 'Total Bookings', 'fieldname': 'total_bookings', 'fieldtype': 'Int', 'width': 110},
        {'label': 'Sabre Share %', 'fieldname': 'sabre_share', 'fieldtype': 'Float', 'width': 110},
    ]

    rows = frappe.db.sql("""
        SELECT
            a.name AS agency,
            a.iata AS iata,
            a.pcc AS pcc,
            a.portfolio_status AS status,
            a.account_manager AS account_manager,
            a.email AS email,
            IFNULL((SELECT SUM(m.sabre_bookings) FROM `tabMIDT Record` m WHERE m.iata = a.iata), 0) AS sabre_bookings,
            IFNULL((SELECT SUM(m.total_bookings) FROM `tabMIDT Record` m WHERE m.iata = a.iata), 0) AS total_bookings
        FROM `tabSabre Agency` a
        {where_clause}
        ORDER BY a.portfolio_status, a.agency_name
    """.format(where_clause=where_clause), values, as_dict=True)

    data = []
    for r in rows:
        share = round(r.sabre_bookings * 100.0 / r.total_bookings, 1) if r.total_bookings else 0
        if sabre_activity == 'With Sabre Bookings' and r.sabre_bookings <= 0:
            continue
        if sabre_activity == 'No Sabre Bookings' and r.sabre_bookings > 0:
            continue
        r['sabre_share'] = share
        data.append(r)

    return columns, data
