from django.core.management.base import BaseCommand
from drone_destination.utilities.geocoding import get_geocoding, get_distance
from drone_destination import models as drone_models
import logging
log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import new deliveries.'

    def add_arguments(self, parser):
        parser.add_argument('pizza_company_id', nargs='+', type=int)

    def handle(self, *args, **options):
        delivery_file = open("deliveries.csv", "r")
        for pizza_company_id in options['pizza_company_id']:
            try:
                pizza_company = drone_models.PizzaCompany.objects.get(pk=pizza_company_id)
            except drone_models.PizzaCompany.DoesNotExist:
                log.error("Trying to import delivery for a pizza company that does not exist.")
                self.stdout.write(f"Failed adding.")
                raise Exception
            for delivery in delivery_file:
                delivery_info = delivery.split(",")
                if len(delivery_info) != 5:
                    self.stdout.write(f"Failed adding record. {delivery_info}")
                else:
                    add_delivery(delivery_info, pizza_company)

            self.stdout.write(self.style.SUCCESS(f"Success provisioning application"))


def add_delivery(delivery_info: list, pizza_company: drone_models.PizzaCompany):
    address = f"{delivery_info[1]} {delivery_info[2]} {delivery_info[3]}, {delivery_info[4]}"
    lat_of_delivery_location, long_of_delivery_location = get_geocoding(address)

    delivery = drone_models.Delivery()
    delivery.pizza_company = pizza_company
    delivery.address = address
    delivery.status = "pending"

    delivery.gps_lat = lat_of_delivery_location
    delivery.gps_long = long_of_delivery_location
    delivery.distance_to_home = get_distance(lat_of_delivery_location, long_of_delivery_location,
                                             pizza_company.gps_lat, pizza_company.gps_long)
    delivery.order_date = delivery_info[0]
    delivery.save()
