import frappe
import json
import os

def import_workspace():
    fixture_path = os.path.join(
        frappe.get_app_path("sabre_sales"), "fixtures", "workspace.json"
    )
    
    if not os.path.exists(fixture_path):
        return

    with open(fixture_path) as f:
        data = json.load(f)

    for workspace in data:
        if frappe.db.exists("Workspace", workspace["name"]):
            frappe.delete_doc("Workspace", workspace["name"], force=True)
        doc = frappe.get_doc(workspace)
        doc.insert(ignore_permissions=True, ignore_links=True)
    
    frappe.db.commit()
    print("Workspace imported successfully")
