# Generated by Django 4.2.7 on 2023-11-15 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startpage', '0006_remove_order_address_address_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryoption',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]