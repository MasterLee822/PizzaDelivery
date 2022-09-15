import requests
from math import *
GOOGLE_API_KEY = "GDSHGHJGSDJHTUYTGHKJ"


def get_geocoding(address):
    lat, lng = None, None
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        return 0,0
    return lat, lng


def get_distance(lat1, lon1, lat2, lon2):
    # Pulled from here:
    # https://stackoverflow.com/questions/45479728/calculate-distance-between-2-points-in-google-maps-using-python
    def haversin(x):
        return sin(x/2)**2
    return 2 * asin(sqrt(
      haversin(lat2-lat1) +
      cos(lat1) * cos(lat2) * haversin(lon2-lon1)))