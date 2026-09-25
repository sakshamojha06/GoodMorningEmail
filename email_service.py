import os
import smtplib

from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

def send_good_morning_email(name, recipient_email):

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    message = EmailMessage()

    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Good Morning!"

    message.set_content(
        f"""Good morning {name}!

        Have a great day ahead.

        Best regards,
        Good Morning Automation
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(message)

    print(f"Email sent successfully to {recipient_email}")