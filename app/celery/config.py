import os

CELERY_BACKEND_ADDRESS = os.getenv('CELERY_BACKEND_ADDRESS', '172.24.96.1')
CELERY_BACKEND_DB = os.getenv('CELERY_BACKEND_DB', 2)

CELERY_BROKER_ADDRESS = os.getenv('CELERY_BROKER_ADDRESS', '172.24.96.1')
CELERY_BROKER_DB = os.getenv('CELERY_BROKER_DB', 1)

CELERY_BACKEND = f'redis://{CELERY_BACKEND_ADDRESS}:6379/{CELERY_BACKEND_DB}'
CELERY_BROKER = f'redis://{CELERY_BROKER_ADDRESS}:6379/{CELERY_BROKER_DB}'

MAIL_SMTP_SERVER = os.getenv('MAIL_SMTP_SERVER')
MAIL_SMTP_LOGIN = os.getenv('MAIL_SMTP_LOGIN')
MAIL_SMTP_PASSWORD = os.getenv('MAIL_SMTP_PASSWORD')