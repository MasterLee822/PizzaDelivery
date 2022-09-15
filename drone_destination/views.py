from django.http import JsonResponse
from drone_destination import models as drone_models
import logging
from datetime import datetime
from drone_destination.utilities.geocoding import get_distance

log = logging.getLogger(__name__)


def get_next_destination(request, drone_token):
    try:
        drone = drone_models.Drone.objects.get(access_key=drone_token)
    except drone_models.Drone.DoesNotExist:
        message = f"Drone does not exist."
        log.error(message)
        return JsonResponse(package_response(True, message))
    distance_from_home = complete_mission_and_return_distance_from_home(drone)
    next_coordinates, message = get_new_mission(drone, distance_from_home)
    return JsonResponse(package_response(False, message, next_coordinates))


def update_drone_status(drone: drone_models.Drone, status:str):
    drone.status = status
    drone.save()


def update_delivery_status(delivery: drone_models.Delivery, status: str):
    delivery.status = status
    delivery.save()


def get_new_mission(drone: drone_models.Drone, distance_from_home: int) -> (str, str):
    drone.set_current_location()
    drone.set_latest_remaining_range()
    drone_range = drone.latest_remaining_range

    if distance_from_home > drone_range:
        update_drone_status(drone, 'not_enough_fuel_to_get_home')
        message = "Drone does not have enough power to go home.  I'm going to stay here until I get help."
        log.critical(message)
        return "0.0,0.0", message

    next_delivery = drone_models.Delivery.objects.filter(
        pizza_company=drone.pizza_company).order_by('-order_date').first()

    if next_delivery:
        distance_to_next_delivery = get_distance(drone.gps_lat, drone.gps_long,
                                                 next_delivery.gps_lat, next_delivery.gps_long)
        total_trip_miles_for_next_mission = distance_to_next_delivery + next_delivery.distance_to_home
        if total_trip_miles_for_next_mission > drone_range:
            return find_alternate_missions(drone)
        else:
            update_delivery_status(next_delivery, 'en_route')
            update_drone_status(drone, 'en_route_for_delivery')
            return f"{next_delivery.gps_lat},{next_delivery.gps_long}", "I've got a new mission to fulfill."
    else:
        if distance_from_home == 0:
            update_drone_status(drone, 'home_base')
            return "0.0,0.0", "No new missions, I'm staying home."
        else:
            gps_string = f"{drone.pizza_company.gps_lat}{drone.pizza_company.gps_long}"
            update_drone_status(drone, 'en_route_for_recharging')
            return gps_string, "No new missions, I'm going home."


def find_alternate_missions(drone: drone_models.Drone) -> (str, str):
    drone_range = drone.latest_remaining_range
    deliveries = drone_models.Delivery.objects.filter(pizza_company=drone.pizza_company).order_by('-order_date')

    for delivery in deliveries:
        distance_to_next_delivery = get_distance(drone.gps_lat, drone.gps_long, delivery.gps_lat, delivery.gps_long)
        total_trip_miles_for_next_mission = distance_to_next_delivery + delivery.distance_to_home
        if total_trip_miles_for_next_mission < drone_range:
            update_delivery_status(delivery, 'en_route')
            update_drone_status(drone, 'en_route_for_delivery')
            return f"{delivery.gps_lat},{delivery.gps_long}", "I've got a new mission to fulfill."

    update_drone_status(drone, 'en_route_for_recharging')
    return f"{drone.pizza_company.gps_lat},{drone.pizza_company.gps_long}", "I'm out of batteries I need to go home."


def complete_mission_and_return_distance_from_home(drone: drone_models.Drone) -> int:
    try:
        delivery = drone_models.Delivery.objects.get(assigned_drone=drone)
    except drone_models.Delivery.DoesNotExist:
        return 0
    except drone_models.Delivery.MultipleObjectsReturned:
        # TODO: Discuss what we would do here
        log.critical(f"A drone is assigned to multiple deliveries. This is not allowed. Drone ID:{drone.pk}")
        raise Exception

    distance_from_home = delivery.distance_to_home

    delivery.status = 'delivered'
    delivery.delivery_complete = datetime.now()
    delivery.save()

    fmt = '%Y-%m-%d %H:%M:%S'
    d1 = datetime.strptime(delivery.delivery_start, fmt)
    d2 = datetime.strptime(delivery.delivery_complete, fmt)
    running_time_minutes = (d2-d1).days * 24 * 60
    drone.add_running_hours(running_time_minutes)
    delivery.archive()
    return distance_from_home



def package_response(error: bool, message, gps_coordinates="0.0,0.0"):
    data = {
        'error': error,
        'message': message,
        'gps_coordinates': gps_coordinates
    }
    return data
