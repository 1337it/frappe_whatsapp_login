import frappe, random, requests, re

def normalize_phone(number: str) -> str:
    """Normalize phone number to E.164 format for WhatsApp"""
    # Remove spaces, dashes, parentheses
    number = re.sub(r'\D', '', number)

    # Rule 1: Starts with + → leave as is
    if number.startswith('+'):
        return number

    # Rule 2: Starts with 00 → replace with +
    if number.startswith('00'):
        return f"+{number[2:]}"

    # Rule 3: UAE local starting with 0 → remove 0 and prepend +971
    if number.startswith('0'):
        return f"+971{number[1:]}"

    # Rule 4: Starts with 971 → prepend +
    if number.startswith('971'):
        return f"+{number}"

    # Fallback: just prepend +
    return f"+{number}"


@frappe.whitelist(allow_guest=True)
def send_otp(number):
    """Send OTP to WhatsApp number"""
    normalized_number = normalize_phone(number)

    # Lookup user by any format stored in DB
    user = frappe.db.get_value(
        "User",
        {"whatsapp_number": normalized_number},
        ["name"],
        as_dict=True
    )
    if not user:
        return {"status": "error", "message": "Number not registered"}

    otp = str(random.randint(100000, 999999))
    frappe.cache().set_value(f"otp_{normalized_number}", otp, expires_in_sec=300)  # 5 mins

    # Capture actual WhatsApp response
    api_response = send_whatsapp_message(normalized_number, otp)

    return {
        "status": "success",
        "message": "OTP sent",
        "normalized_number": normalized_number,
        "whatsapp_response": api_response
    }


@frappe.whitelist(allow_guest=True)
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
        "to": number,  # Always normalized
        "type": "template",
        "template": {
            "name": "otp_login",  # Your approved template
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
    frappe.logger().info(res.text)  # Logs response in bench
    try:
        return res.json()
    except:
        return {"error": res.text}


@frappe.whitelist(allow_guest=True)
def verify_otp(number, otp):
    """Verify OTP and log user in"""
    normalized_number = normalize_phone(number)

    saved_otp = frappe.cache().get_value(f"otp_{normalized_number}")
    if not saved_otp or saved_otp != otp:
        return {"status": "error", "message": "Invalid or expired OTP"}

    user = frappe.db.get_value(
        "User",
        {"whatsapp_number": ["in", [number, normalized_number]]},
        ["name"]
    )
    if not user:
        return {"status": "error", "message": "User not found"}

    # Log in user
    frappe.local.login_manager.user = user
    frappe.local.login_manager.post_login()
    frappe.db.commit()
    return {"status": "success", "message": "Login successful"}
    
@frappe.whitelist(allow_guest=True)
def send_network_alert(number, message):
    """
    Send WhatsApp message to the given number.
    Example: Called from Orange Pi network scanner.
    """
    # Format number if needed
    if number.startswith("00"):
        number = "+" + number[2:]
    elif not number.startswith("+"):
        number = "+" + number

    # Use your existing WhatsApp sending logic here
    try:
        # Example: insert a WhatsApp Message doc if your app uses that
        doc = frappe.get_doc({
            "doctype": "WhatsApp Message",
            "receiver": number,
            "message": message
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": f"WhatsApp sent to {number}"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "WhatsApp Send Error")
        return {"status": "error", "message": str(e)}
