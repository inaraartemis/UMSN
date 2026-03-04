import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

logger = logging.getLogger(__name__)

# Note: In a production environment, these should be in .env
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using SMTP.
    In a real production environment, this would use a background task worker like Celery.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning(f"SMTP credentials not set. Simulating email to {to_email}: {subject}")
        print(f"DEBUG: Email to {to_email} | Subject: {subject} | Body: {body}")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")

def notify_registration(email: str, token: str):
    subject = "Verify your account - Smart Hostel"
    body = f"Welcome to Smart Hostel! Please verify your account using this token: {token}"
    send_email(email, subject, body)

def notify_room_allocation(email: str, room_number: str):
    subject = "Room Allocated - Smart Hostel"
    body = f"Congratulations! You have been allocated room {room_number}."
    send_email(email, subject, body)

def notify_complaint_update(email: str, complaint_title: str, status: str):
    subject = f"Complaint Update: {complaint_title}"
    body = f"Your complaint '{complaint_title}' has been updated to: {status}."
    send_email(email, subject, body)
