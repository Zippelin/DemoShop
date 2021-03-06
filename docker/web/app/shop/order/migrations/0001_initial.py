# Generated by Django 3.2.7 on 2021-09-08 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('street', models.CharField(max_length=255, verbose_name='Улица')),
                ('house_number', models.IntegerField(verbose_name='Номер дома')),
                ('housing', models.IntegerField(blank=True, null=True, verbose_name='Строение')),
                ('structure', models.IntegerField(blank=True, null=True, verbose_name='Корпус')),
                ('apartment', models.CharField(max_length=20, verbose_name='Квартира или Офис')),
                ('additional_info', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Дополнительная информация')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('status', models.CharField(choices=[('NEW', 'NEW'), ('IN_PROGRESS', 'IN_PROGRESS'), ('DONE', 'DONE'), ('CANCELED', 'CANCELED')], max_length=20, verbose_name='Статус')),
                ('recipient_email', models.EmailField(max_length=255, unique=True, verbose_name='Электронная почта')),
                ('recipient_first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('recipient_last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('recipient_patronymic', models.CharField(max_length=255, verbose_name='Отчество')),
                ('recipient_phone', models.CharField(max_length=50, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
