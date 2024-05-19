from celery import Celery
import smtplib
from email.message import EmailMessage
from api.config import email_config, rabbit_config

celery_app = Celery(
    broker='amqp://guest:guest@localhost:5672//',
    backend='rpc://',
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
        subtype = 'html'
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_config.APP_EMAIL, email_config.SECRET_MAIL)
        smtp.send_message(msg)