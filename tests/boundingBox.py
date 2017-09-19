
import numpy as np

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from googlestaticmaps.provider import get_map_at_lonlat


with open("googlemaps_apikey.txt") as fh:
    gapikey = fh.read()
    fh.close()

with open("bingmaps_apikey.txt") as fh:
    bapikey = fh.read()
    fh.close()


def get_bing_bbox(lon, lat, zoom, imgSize):

    from requests.sessions import Session

    # Build URL
    url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/"
    url += str(lat) + "," + str(lon) + "/" + str(zoom)

    url += "?" + urlencode({
        'mapSize': ",".join(str(x) for x in imgSize),
        'mapLayer': '',
        'mapMetadata': '1',
        'key': bapikey
    })

    response = Session().get(url)

    if response.status_code != 200:
        return False

    json_data = response.json()

    return [float(x) for x in json_data['resourceSets'][0]['resources'][0]['bbox']]


def bingmaps(lon, lat, zoom, imgSize):
    """ Bing uses the same projection and zoom levels and returns the bbox as meta data """

    expectedResult = get_bing_bbox(lon, lat, zoom, imgSize)
    #result = get_map_at_lonlat(lon, lat, zoom, apikey=gapikey, imgSize=imgSize).boundingBox.list

    from googlestaticmaps.boundingBox import BoundingBox
    result = BoundingBox.createFromCenterPointLonLat(lon, lat, zoom, imgSize).list

    if not np.allclose(result, expectedResult, rtol=1.e-4, atol=1.e-8):
        return False

    return True


# Test 1
print("Test #1")

lat = 48.2
lon = 11.3
zoom = 12
imgSize = (256, 256)

if bingmaps(lon, lat, zoom, imgSize):
    print(" ... ok!")
else:
    print(" ... not ok!")


# Test 2
print("Test #2")

lat = 48.2
lon = 11.3
zoom = 19
imgSize = (256, 256)

if bingmaps(lon, lat, zoom, imgSize):
    print(" ... ok!")
else:
    print(" ... not ok!")


# Test 3
print("Test #3")

lat = 48.2
lon = 11.3
zoom = 19
imgSize = (500, 500)

if bingmaps(lon, lat, zoom, imgSize):
    print(" ... ok!")
else:
    print(" ... not ok!")
