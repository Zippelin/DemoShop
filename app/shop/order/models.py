from django.db import models
from django.utils.translation import gettext_lazy as _
from profile.models import AddressAbstractModel
from assortment.models import Assortment


class Order(AddressAbstractModel):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    class Status(models.TextChoices):
        NEW = "NEW", _("NEW")
        IN_PROGRESS = "IN_PROGRESS", _("IN_PROGRESS")
        DONE = "DONE", _("DONE")
        CANCELED = "CANCELED", _("CANCELED")

    date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    status = models.CharField(choices=Status.choices, verbose_name='Статус', max_length=20)
    recipient_email = models.EmailField(verbose_name='Электронная почта', max_length=255, unique=True)
    recipient_first_name = models.CharField(verbose_name='Имя', max_length=255)
    recipient_last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    recipient_patronymic = models.CharField(verbose_name='Отчество', max_length=255)
    recipient_phone = models.CharField(verbose_name='Телефон', max_length=50)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE
    )
    assortment = models.ForeignKey(
        Assortment,
        verbose_name='Товар',
        on_delete=models.DO_NOTHING
    )
    quantity = models.IntegerField(verbose_name='Кол-во', default=1)
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Цена',
        default=1
    )
