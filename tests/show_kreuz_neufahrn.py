
from googlestaticmaps.provider import get_map_at_latlon, GoogleMapType


with open("googlemaps_apikey.txt") as fh:
    apikey = fh.read()
    fh.close()

img = get_map_at_latlon(48.316362, 11.620967, 16, (700, 700), apikey, mapType=GoogleMapType.Hybrid).mapImage
img.show()
