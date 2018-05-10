import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient, email_text):
    msg = MIMEMultipart()
    msg['Subject'] = 'You\'re a match'
    msg['From'] = 'metatinder@metaswitch.com'
    msg['To'] = recipient
    msg.attach(MIMEText(email_text))
    s = smtplib.SMTP('int-smtp')
    s.sendmail("metatinder@metaswitch.com", "thomas.cappleman@metaswitch.com", msg.as_string())
    s.quit()
