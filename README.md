# Frappe WhatsApp Login

A custom Frappe app to enable **WhatsApp OTP-based login** for ERPNext and Frappe sites.

---

## Features

- Login users via **WhatsApp OTP** instead of email/password.
- **5-minute OTP expiration** with caching.
- **WhatsApp Cloud API** integration (can adapt to Twilio/Gupshup).
- Optional **standalone web login page** at `/whatsapp-login`.

---

## Requirements

- Frappe v14+ (tested)
- Python `requests` library
- WhatsApp Cloud API credentials
  - `phone_id`
  - `api_token` (permanent or temporary access token)

---

## Installation

1. **Get the app:**

```bash
cd ~/frappe-bench/apps
git clone https://your-repo/frappe_whatsapp_login.git
