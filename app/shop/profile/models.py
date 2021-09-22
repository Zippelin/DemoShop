from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class Position(models.Model):

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    name = models.CharField(verbose_name='Наименование', max_length=150, unique=True)


class Company(models.Model):

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    name = models.CharField(verbose_name='Наименование', max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    class Type(models.TextChoices):
        CUSTOMER = "CUSTOMER", _("CUSTOMER")
        PROVIDER = "PROVIDER", _("PROVIDER")

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=255,
        unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=255, null=False, blank=False)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255, null=False, blank=False)
    patronymic = models.CharField(verbose_name='Отчество', max_length=255)
    phone = models.CharField(verbose_name='Телефон', max_length=50)
    position = models.ForeignKey(
        Position,
        verbose_name='Должность',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    company = models.ForeignKey(
        Company,
        verbose_name='Организация',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    type = models.CharField(
        choices=Type.choices,
        verbose_name='Тип пользователя',
        max_length=15,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save()


class Address(models.Model):

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    city = models.CharField(verbose_name='Город', max_length=255)
    street = models.CharField(verbose_name='Улица', max_length=255)
    house_number = models.IntegerField(verbose_name='Номер дома')
    housing = models.IntegerField(verbose_name='Строение', blank=True, null=True)
    structure = models.IntegerField(verbose_name='Корпус', blank=True, null=True)
    apartment = models.CharField(verbose_name='Квартира или Офис', max_length=20)
    additional_info = models.TextField(
        verbose_name='Дополнительная информация',
        blank=True,
        null=True,
        max_length=1000
    )
