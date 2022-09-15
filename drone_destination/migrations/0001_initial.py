# Generated by Django 4.1.1 on 2022-09-15 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PizzaCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('gps_lat', models.CharField(max_length=255)),
                ('gps_long', models.CharField(max_length=255)),
                ('date_inserted', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('mac_address', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(blank=True, choices=[('home_base', 'Home Base'), ('en_route_for_delivery', 'Off for delivery'), ('en_route_for_recharging', 'En route to recharge')], max_length=255)),
                ('access_key', models.CharField(max_length=255)),
                ('refresh_key', models.CharField(max_length=255)),
                ('total_running_hours', models.IntegerField(default=0)),
                ('latest_remaining_range', models.IntegerField(default=0)),
                ('location_of_last_request', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('token_expiration', models.DateTimeField(blank=True, null=True)),
                ('date_inserted', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('pizza_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drone_destination.pizzacompany')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, choices=[('pending', 'Home Base'), ('en_route', 'Pizza on its way'), ('delivered', 'Delivered')], max_length=255)),
                ('gps_lat', models.CharField(max_length=255)),
                ('gps_long', models.CharField(max_length=255)),
                ('distance_to_home', models.IntegerField(default=0)),
                ('order_date', models.DateTimeField(blank=True, null=True)),
                ('date_inserted', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('assigned_drone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drone_destination.drone')),
            ],
        ),
    ]
