import frappe

def after_install():
    """Create whatsapp_number field in User doctype if it doesn't exist"""
    if not frappe.db.exists("Custom Field", {"dt": "User", "fieldname": "whatsapp_number"}):
        cf = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "User",
            "fieldname": "whatsapp_number",
            "label": "WhatsApp Number",
            "fieldtype": "Data",
            "insert_after": "phone",  # or any existing field
            "unique": 1
        })
        cf.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger().info("Created whatsapp_number field in User doctype")
