
from functools import lru_cache
from enum import Enum
from io import BytesIO

from PIL import Image
from requests.sessions import Session

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


from googlestaticmaps.map import Map
from googlestaticmaps.boundingBox import BoundingBox


class GoogleMapType(Enum):
    Roadmap = "roadmap"
    Satellite = "satellite"
    Hybrid = "hybrid"
    Terrain = "terrain"
    Dummy = "dummy"


def generate_url(lat, lon, zoom, imgSizeX, imgSizeY, apikey, mapType=GoogleMapType.Satellite):

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

@lru_cache(maxsize=320000)
def download_image(request_url):
    session = Session()

    try:
        response = session.get(request_url)
    finally:
        session.close()

    if response.status_code != 200:
        raise Exception("Error while downloading map from Google Maps API.")

    return Image.open(BytesIO(response.content))


def get_map_at_lonlat(lon, lat, zoom, apikey, imgSize=(256, 256), mapType=GoogleMapType.Satellite):

    # Get apikey from env
    if apikey is None:
        import os
        apikey = os.getenv("GOOGLEMAPS_STATICMAP_APIKEY")

    # Start API request
    request_url = generate_url(lat, lon, zoom, imgSize[0], imgSize[1], apikey, mapType)

    if mapType == GoogleMapType.Dummy:
        img = Image.new('RGB', imgSize, (70, 70, 70))
    else:
        img = download_image(request_url)


    # Calculate bounding box
    bbox = BoundingBox.createFromCenterPointLonLat(lon, lat, zoom, img.size)

    return Map(img, (lon, lat), zoom, bbox)
