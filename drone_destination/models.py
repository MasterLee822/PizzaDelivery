from django.db import models

# Create your models here.
# date_inserted
# address
# distance_from_home

DRONE_STATUS = (
    (u'home_base', u'Home Base'),
    (u'en_route_for_delivery', u'Off for delivery'),
    (u'en_route_for_recharging', u'En route to recharge'),
    (u'not_enough_fuel_to_get_home', u'Out of Fuel'),
)

DELIVERY_STATUS = (
    (u'pending', u'Home Base'),
    (u'en_route', u'Pizza on its way'),
    (u'delivered', u'Delivered'),
)


class PizzaCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)
    street_address = models.CharField(max_length=255, blank=True)
    gps_lat = models.CharField(max_length=255)
    gps_long = models.CharField(max_length=255)
    date_inserted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Drone(models.Model):
    name = models.CharField(max_length=255, unique=True)
    pizza_company = models.ForeignKey(PizzaCompany,on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=DRONE_STATUS, blank=True)
    access_key = models.CharField(max_length=255)
    refresh_key = models.CharField(max_length=255)
    total_running_hours = models.IntegerField(default=0)
    latest_remaining_range = models.IntegerField(default=0)
    gps_lat = models.CharField(max_length=255)
    gps_long = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)
    token_expiration = models.DateTimeField(blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def can_make_it_to_destination(self, distance) -> bool:
        if self.latest_remaining_range > distance:
            return True
        else:
            return False

    def set_current_location(self):
        # Go to whatever API to get this value
        self.location_of_last_request = "0.0,0.0"
        self.save()

    def set_latest_remaining_range(self):
        # Go to whatever API to get this value
        self.latest_remaining_range = 10
        self.save()

    def add_running_hours(self, hours):
        # Go to whatever API to get this value
        self.total_running_hours += hours
        self.save()


class Delivery(models.Model):
    address = models.CharField(max_length=255)
    pizza_company = models.ForeignKey(PizzaCompany, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=DELIVERY_STATUS, blank=True)
    gps_lat = models.CharField(max_length=255)
    gps_long = models.CharField(max_length=255)
    distance_to_home = models.IntegerField(default=0)
    assigned_drone = models.ForeignKey(Drone, on_delete=models.CASCADE, blank=True, null=True, unique=True)
    order_date = models.DateTimeField(blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    delivery_start = models.DateTimeField(blank=True, null=True)
    delivery_complete = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.address}"

    def archive(self):
        # Send off to NOSQL DB for machine learning
        self.delete()



