# Generated by Django 3.2.7 on 2021-09-13 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_category'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productfeature',
            unique_together={('product', 'feature', 'value')},
        ),
    ]
