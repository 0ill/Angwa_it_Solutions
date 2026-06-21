"""
utils/email.py – SMTP email sender.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(to: str, subject: str, body: str, html_body: str = None) -> bool:
    """Send an email via SMTP."""
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", 587))
    username = os.environ.get("SMTP_USERNAME")
    password = os.environ.get("SMTP_PASSWORD")
    from_addr = os.environ.get("SMTP_FROM", username)

    if not username or not password:
        raise RuntimeError("SMTP credentials not set.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to

    part_text = MIMEText(body, "plain")
    msg.attach(part_text)
    if html_body:
        part_html = MIMEText(html_body, "html")
        msg.attach(part_html)

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(from_addr, [to], msg.as_string())
    return True

def send_order_confirmation(to_email: str, order_id: int, customer_name: str, total: float, items_summary: str) -> bool:
    subject = f"ANGWA Order Confirmation #{order_id}"
    body = f"""
Hi {customer_name},

Thank you for your order (#{order_id}).

Total: R{total:.2f}
Items: {items_summary}

We'll notify you once your order is processed.

- The ANGWA Team
"""
    html_body = f"""
<html><body>
<h2>Order Confirmation #{order_id}</h2>
<p>Hi {customer_name},</p>
<p>Thank you for your order.</p>
<p><strong>Total:</strong> R{total:.2f}</p>
<p><strong>Items:</strong> {items_summary}</p>
<p>We'll notify you when it's processed.</p>
<p>- The ANGWA Team</p>
</body></html>
"""
    return send_email(to_email, subject, body, html_body)
