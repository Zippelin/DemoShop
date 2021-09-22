import allauth
from django.dispatch import receiver, Signal
from utils.response import get_mail_text_on_order_creation, get_mail_text_on_sing_up
try:
    import app.celery.tasks as tasks
except ImportError:
    pass

new_user_registration = Signal(
    providing_args=['user_id']
)

new_order_confirmation = Signal(
    providing_args=[
        'order_number', 'order_url', 'to_address', 'to_address', 'last_name', 'first_name'
    ]
)


@receiver(new_order_confirmation)
def send_order_confirmation_mail(order_url, order_number, to_address, last_name, first_name, **kwargs):
    mail_text, mail_header = get_mail_text_on_order_creation(order_url, order_number, last_name, first_name)
    tasks.send_mail.delay(to_address, mail_header, mail_text)


@receiver(allauth.account.signals.user_signed_up)
def send_email_on_registration_confirmation(request, user, **kwargs):
    mail_text, mail_header = get_mail_text_on_sing_up(user.email)
    tasks.send_mail.delay(user.email, mail_header, mail_text)
