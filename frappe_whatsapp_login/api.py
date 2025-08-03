import frappe, random, requests

@frappe.whitelist(allow_guest=True)
def send_otp(number):
    """Send OTP to WhatsApp number"""
    user = frappe.db.get_value("User", {"whatsapp_number": number}, ["name"], as_dict=True)
    if not user:
        return {"status": "error", "message": "Number not registered"}

    otp = str(random.randint(100000, 999999))
    frappe.cache().set_value(f"otp_{number}", otp, expires_in_sec=300)  # 5 mins

    res = send_whatsapp_message(number, otp)
    return {"status": "success", "message": "OTP sent", "response": res}


def send_whatsapp_message(number, otp):
    """Send OTP using WhatsApp Template Message (Cloud API)"""
    token = frappe.db.get_single_value("WhatsApp Settings", "token")
    phone_id = frappe.db.get_single_value("WhatsApp Settings", "phone_id")
    
    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": number,  # e.g. +971500000000
        "type": "template",
        "template": {
            "name": "otp_login",  # Change to your approved template name
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": otp}
                    ]
                }
            ]
        }
    }

    res = requests.post(url, json=payload, headers=headers)
    try:
        return res.json()
    except:
        return {"error": res.text}


@frappe.whitelist(allow_guest=True)
def verify_otp(number, otp):
    """Verify OTP and log user in"""
    saved_otp = frappe.cache().get_value(f"otp_{number}")
    if not saved_otp or saved_otp != otp:
        return {"status": "error", "message": "Invalid or expired OTP"}

    user = frappe.db.get_value("User", {"whatsapp_number": number}, ["name"])
    if not user:
        return {"status": "error", "message": "User not found"}

    # Log in user
    frappe.local.login_manager.user = user
    frappe.local.login_manager.post_login()
    frappe.db.commit()
    return {"status": "success", "message": "Login successful"}
