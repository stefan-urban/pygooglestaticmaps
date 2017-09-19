
from googlestaticmaps import get_map_at_lonlat, GoogleMapType


# Get google maps apikey
try:
    with open("googlemaps_apikey.txt") as fh:
        googlemaps_apikey = fh.read()
        fh.close()
except IOError:
    print("No google maps apikey found!")
    quit(-1)

img = get_map_at_lonlat(11.620967, 48.316362, 16, apikey=apikey, imgSize=(700, 700), mapType=GoogleMapType.Hybrid).mapImage
img.show()
