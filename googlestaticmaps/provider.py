
from enum import Enum

from PIL import Image
from io import StringIO, BytesIO
from requests.sessions import Session
from requests_futures.sessions import FuturesSession

try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode


from googlestaticmaps.map import Map
from googlestaticmaps.boundingBox import BoundingBox

class GoogleMapType(Enum):
    Roadmap = "roadmap"
    Satellite = "satellite"
    Hybrid = "hybrid"
    Terrain = "terrain"


def generate_url(lat, lon, zoom, imgSizeX, imgSizeY, mapType=GoogleMapType.Satellite, apikey=None):

    # Start download from Google Maps
    url = "https://maps.googleapis.com/maps/api/staticmap"

    try:
        mapTypeStr = mapType.value
    except AttributeError:
        mapTypeStr = str(mapType)

    payload = {
        'center': str(lat) + "," + str(lon),
        'zoom': str(zoom),
        'format': 'png32',
        'size': str(imgSizeX) + "x" + str(imgSizeY),
        'scale': '1',
        'maptype': mapTypeStr,
        'key': apikey,
        #'markers': 'color:blue|label:S|48.268336,11.645252',
    }

    return url + "?" + urlencode(payload)


def get_map_at_latlon(lat, lon, zoom, imgSize=(500, 500), apikey=None, mapType=GoogleMapType.Satellite):

    # Get apikey from env
    if apikey is None:
        import os
        apikey = os.getenv("GOOGLEMAPS_STATICMAP_APIKEY")

    # Start API request
    session = Session()
    response = session.get(generate_url(lat, lon, zoom, imgSize[0], imgSize[1], mapType, apikey))

    if response.status_code != 200:
        raise Exception("Error while downloading map from Google Maps API.")

    img = Image.open(BytesIO(response.content))

    # Calculate bounding box
    bbox = BoundingBox.createFromCenterPoint(lat, lon, zoom, img.size)

    return Map(img, (lat, lon), zoom, bbox)
