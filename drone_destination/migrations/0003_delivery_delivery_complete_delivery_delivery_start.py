# Generated by Django 4.1.1 on 2022-09-15 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drone_destination', '0002_delivery_pizza_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='delivery_complete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
