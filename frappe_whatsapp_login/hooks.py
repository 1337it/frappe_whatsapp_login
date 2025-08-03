app_name = "frappe_whatsapp_login"
app_title = "Frappe WhatsApp Login"
app_publisher = "Leet IT Solutions"
app_description = "WhatsApp OTP-based login for Frappe"
app_email = "aman@leetitsolutions.com"
app_version = "0.0.1"

# Expose APIs
override_whitelisted_methods = {
    # None yet
}

# Optional: Add web templates
website_route_rules = [
    {"from_route": "/whatsapp-login", "to_route": "whatsapp_login"},
]
