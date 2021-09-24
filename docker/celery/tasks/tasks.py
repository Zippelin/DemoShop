from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import celery

from config import CELERY_BACKEND, CELERY_BROKER, \
    MAIL_SMTP_SERVER, MAIL_SMTP_LOGIN, MAIL_SMTP_PASSWORD
from smtplib import SMTP

celery_app = celery.Celery(
    'tasks',
    backend=CELERY_BACKEND,
    broker=CELERY_BROKER
)


@celery_app.task()
def send_mail(to_address, header, text):
    server = SMTP(MAIL_SMTP_SERVER)
    conn = server.connect(MAIL_SMTP_SERVER)
    print(conn)
    res = server.ehlo()
    print(res)
    res = server.starttls()
    print(res)
    res = server.ehlo()
    print(res)
    res = server.login(MAIL_SMTP_LOGIN, MAIL_SMTP_PASSWORD)
    print(res)

    msg = MIMEMultipart()
    msg['From'] = MAIL_SMTP_LOGIN
    msg['To'] = to_address
    msg['Subject'] = header

    msg.attach(MIMEText(text, 'plain'))
    text = msg.as_string()

    res = server.sendmail(MAIL_SMTP_LOGIN, MAIL_SMTP_LOGIN, text)
    print(res)

    server.quit()
    return True

