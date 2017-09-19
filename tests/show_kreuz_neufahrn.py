
from googlestaticmaps import get_map_at_lonlat, GoogleMapType


with open("googlemaps_apikey.txt") as fh:
    apikey = fh.read()
    fh.close()

img = get_map_at_lonlat(11.620967, 48.316362, 16, apikey=apikey, imgSize=(700, 700), mapType=GoogleMapType.Hybrid).mapImage
img.show()
