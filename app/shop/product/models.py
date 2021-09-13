from django.db import models


class Product(models.Model):

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(max_length=200, verbose_name='Наименование')
    features = models.ManyToManyField(
        'Feature',
        through='ProductFeature',
        related_name='features'
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f'name: {self.name};'


class Feature(models.Model):

    class Meta:
        verbose_name = 'Хар-ка'
        verbose_name_plural = 'Хар-ки'

    name = models.CharField(max_length=200, verbose_name='Наименование')

    def __str__(self):
        return f'name:{self.name}'


class ProductFeature(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product'
    )

    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        related_name='feature'
    )

    value = models.CharField(max_length=200,
                             verbose_name='Значение',
                             null=True, blank=True
                             )


class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=200, verbose_name='Наименование')