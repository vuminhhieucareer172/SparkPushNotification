import smtplib
import ssl
from email.message import EmailMessage

from backend.schemas.configuration import ConfigEmail


def email_sender(source: ConfigEmail, email_destination: str, subject: str, content: str = '', using_ssl=True):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = source.email
        msg['To'] = email_destination
        msg.set_content(content)
        context = ssl.create_default_context()
        if using_ssl:
            server = smtplib.SMTP_SSL(host=source.host, port=source.port, context=context)
        else:
            server = smtplib.SMTP(host=source.host, port=source.port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        server.login(source.username, source.password)
        server.send_message(msg)
        server.quit()
        return "Completed"
    except Exception as e:
        print(e)
        return "Error: {}".format(str(e))
