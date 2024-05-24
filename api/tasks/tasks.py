from email import encoders
from email.mime.base import MIMEBase
from celery import Celery
import smtplib
from email.message import EmailMessage

from pydantic import EmailStr
from api.config import email_config

celery_app = Celery(
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
)


@celery_app.task
def send_mail(email, title, content):
    msg = EmailMessage()
    msg["Subject"] = title
    msg["From"] = email_config.SECRET_MAIL
    msg["To"] = email

    msg.set_content(
        f""" 

    <div> {content} <div>

         """,
        subtype="html",
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_config.APP_EMAIL, email_config.SECRET_MAIL)
        smtp.send_message(msg)


@celery_app.task
def send_appointments_report(email: EmailStr, title: str, pdf_buffer, pdf_filename):
    msg = EmailMessage()
    msg["Subject"] = title
    msg["From"] = email_config.SECRET_MAIL
    msg["To"] = email
    part = MIMEBase("application", "octet-stream")
    part.set_payload(pdf_buffer.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={pdf_filename}")
    msg.add_attachment(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_config.APP_EMAIL, email_config.SECRET_MAIL)
        smtp.send_message(msg)
