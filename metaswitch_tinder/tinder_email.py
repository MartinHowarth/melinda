import smtplib

from typing import List

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sendgrid
import os
from sendgrid.helpers.mail import *


def send_email(recipients: List[str], email_text):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('metatinder@metaswitch.com')
    subject = 'You\'re a match'
    to_email = Email(recipients[0])
    content = Content("text/plain", email_text)
    mail = Mail(from_email, subject, to_email, content)
    for recip in recipients[1:]:
        mail.personalizations[0].add_to(Email(recip))
    response = sg.client.mail.send.post(request_body=mail.get())
    # msg = MIMEMultipart()
    # msg['Subject'] = 'You\'re a match'
    # msg['From'] = 'metatinder@metaswitch.com'
    # msg['To'] = ','.join(recipients)
    # msg.attach(MIMEText(email_text))
    # s = smtplib.SMTP('int-smtp')
    # s.sendmail("metatinder@metaswitch.com", recipients, msg.as_string())
    # s.quit()


def send_report_email(email_text):
    msg = MIMEMultipart()
    msg['Subject'] = 'Metaswitch Tinder User Report'
    msg['From'] = 'metatinder@metaswitch.com'
    msg['To'] = ',metatinder@gmail.com'
    msg.attach(MIMEText(email_text))
    s = smtplib.SMTP('int-smtp')
    s.sendmail('metatinder@metaswitch.com', 'metatinder@gmail.com', msg.as_string())
    s.quit()
