from django.db import models
from django.utils.translation import gettext_lazy as _
from profile.models import User
from assortment.models import Assortment


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    class Status(models.TextChoices):
        NEW = "NEW", _("NEW")
        IN_PROGRESS = "IN_PROGRESS", _("IN_PROGRESS")
        DONE = "DONE", _("DONE")
        CANCELED = "CANCELED", _("CANCELED")

    date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    status = models.CharField(
        choices=Status.choices,
        verbose_name='Статус',
        max_length=20,
        default=Status.NEW
    )
    recipient_email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=255,
        null=True, blank=True
    )
    recipient_first_name = models.CharField(
        verbose_name='Имя',
        max_length=255,
        null=True, blank=True
    )
    recipient_last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
        null=True, blank=True
    )
    recipient_patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=255,
        null=True, blank=True
    )
    recipient_phone = models.CharField(
        verbose_name='Телефон',
        max_length=50,
        null=True, blank=True
    )
    profile = models.ForeignKey(
        User,
        verbose_name='Заказавший',
        on_delete=models.DO_NOTHING,
        related_name='orders'
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=255,
        null=True, blank=True
    )
    street = models.CharField(
        verbose_name='Улица',
        max_length=255,
        null=True, blank=True
    )
    house_number = models.IntegerField(
        verbose_name='Номер дома',
        null=True, blank=True
    )
    housing = models.IntegerField(
        verbose_name='Строение',
        blank=True, null=True
    )
    structure = models.IntegerField(
        verbose_name='Корпус',
        blank=True, null=True
    )
    apartment = models.CharField(
        verbose_name='Квартира или Офис',
        max_length=20,
        null=True, blank=True
    )
    additional_info = models.TextField(
        verbose_name='Дополнительная информация',
        blank=True,
        null=True,
        max_length=1000,
    )

    def get_items_count(self):
        return self.order_items.all().count()

    get_items_count.short_description = 'Кол-во товаров'

    def get_items_sum(self):
        sum = 0
        for item in self.order_items.all():
            sum += item.price * item.quantity

        return sum

    get_items_sum.short_description = 'Сумма заказа'

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='order_items'
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
        default=1,
        null=True,
        blank=True
    )

    def get_company(self):
        return self.assortment.company

    get_company.short_description = 'Компания'
