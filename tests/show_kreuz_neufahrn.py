
from googlestaticmaps.provider import get_map_at_latlon, GoogleMapType


# Get google maps apikey
try:
    with open("googlemaps_apikey.txt") as fh:
        googlemaps_apikey = fh.read()
        fh.close()
except IOError:
    print("No google maps apikey found!")
    quit(-1)


img = get_map_at_latlon(48.316362, 11.620967, 16, (700, 700), googlemaps_apikey, mapType=GoogleMapType.Hybrid).mapImage
img.show()
