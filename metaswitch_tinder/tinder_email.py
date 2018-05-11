import smtplib

from typing import List

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(recipients: List[str], email_text):
    msg = MIMEMultipart()
    msg['Subject'] = 'You\'re a match'
    msg['From'] = 'metatinder@metaswitch.com'
    msg['To'] = ','.join(recipients)
    msg.attach(MIMEText(email_text))
    s = smtplib.SMTP('int-smtp')
    s.sendmail("metatinder@metaswitch.com", recipients, msg.as_string())
    s.quit()
