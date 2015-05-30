from geopy.geocoders import Nominatim
import logging

MAX_TIMEOUT = 5

def get_coords(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address, timeout=MAX_TIMEOUT)
    logging.debug(location)
    return (location.latitude, location.longitude)

def get_address(lat, lon):
    geolocator = Nominatim()
    location = geolocator.reverse(str(lat) + ", " + str(lon))
    return location.address
