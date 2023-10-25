import smtplib
import ssl
from email.message import EmailMessage

from const import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER

PORT = 465
context = ssl.create_default_context()


def generate_email(email: str, body: str) -> EmailMessage:
    """
    Generate an email message with the given email address and body.
    """
    message = EmailMessage()
    message['From'] = EMAIL_HOST_USER
    message['To'] = email
    message.set_content(body)
    return message


def connect_smtp(message: EmailMessage):
    """
    Connects to the SMTP server and sends an email message.
    """
    with smtplib.SMTP_SSL('smtp.yandex.ru', PORT, context=context) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(message)
        server.quit()


def send_email(email: str, body: str):
    """
    Sends an email using the provided `message`.
    """
    try:
        connect_smtp(generate_email(email, body))
    except Exception as e:
        raise e
