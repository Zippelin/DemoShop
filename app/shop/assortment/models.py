from django.db import models
from profile.models import Company
from product.models import Product


class Assortment(models.Model):

    class Meta:
        verbose_name = 'Ассортимент'
        verbose_name_plural = 'Ассортимент'

    company = models.ForeignKey(
        Company,
        verbose_name='Продавец',
        on_delete=models.DO_NOTHING,
        related_name='company_assortment'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.DO_NOTHING,
        related_name='product_assortment'
    )
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Цена',
        default=1
    )
    quantity = models.IntegerField(verbose_name='Кол-во', default=1)
    available = models.BooleanField(default=True, verbose_name='Доступе для продажи')
    description = models.TextField(max_length=20000, verbose_name='Описание', null=True, blank=True)