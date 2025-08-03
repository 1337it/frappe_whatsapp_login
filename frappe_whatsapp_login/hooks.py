app_name = "frappe_whatsapp_login"
app_title = "Frappe WhatsApp Login"
app_publisher = "Leet IT Solutions"
app_description = "WhatsApp OTP-based login for Frappe"
app_email = "aman@leetitsolutions.com"
app_version = "0.0.1"

page_js = {
    "login": "public/js/login_whatsapp.js"
}
app_include_css = []

web_include_js = []
web_include_css = []

# No doctype assets either
doctype_js = {}
doctype_list_js = {}
doctype_tree_js = {}
doctype_calendar_js = {}
# Expose APIs
override_whitelisted_methods = {
    # None yet
}
after_install = "frappe_whatsapp_login.install.after_install"
# Optional: Add web templates
website_route_rules = [
    {"from_route": "/whatsapp-login", "to_route": "whatsapp_login"},
]
