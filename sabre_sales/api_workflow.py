import frappe
from frappe.model.workflow import apply_workflow


@frappe.whitelist()
def apply_opportunity_workflow_action(opportunity, action):
    doc = frappe.get_doc("Sabre Sales Opportunity", opportunity)
    try:
        apply_workflow(doc, action)
    except frappe.exceptions.ValidationError:
        frappe.clear_last_message()
        frappe.throw(
            "This action isn't available for your role right now. It may need to be "
            "completed by another team member, or a required step hasn't been finished yet.",
            title="Action Not Available",
        )
    return {"next_state": doc.workflow_state}
