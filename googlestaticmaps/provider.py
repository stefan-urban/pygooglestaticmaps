
from enum import Enum

from PIL import Image
from io import StringIO, BytesIO
from requests.sessions import Session
from requests_futures.sessions import FuturesSession

from googlestaticmaps.map import Map
from googlestaticmaps.boundingBox import BoundingBox

class GoogleMapType(Enum):
    Roadmap = "roadmap"
    Satellite = "satellite"
    Hybrid = "hybrid"
    Terrain = "terrain"


def get_map_at_latlon(lat, lon, zoom, imgSize=(500, 500), apikey=None, mapType=GoogleMapType.Satellite):

    # Get apikey from env
    if apikey is None:
        import os
        apikey = os.getenv("GOOGLEMAPS_STATICMAP_APIKEY")

    # Start download from Google Maps
    url = "https://maps.googleapis.com/maps/api/staticmap"

    payload = {
        'center': str(lat) + "," + str(lon),
        'zoom': str(zoom),
        'format': 'png32',
        'size': "x".join(str(x) for x in imgSize),
        'scale': '1',
        'maptype': mapType.value,
        'key': apikey,
        #'markers': 'color:blue|label:S|48.268336,11.645252',
    }

    # Start API request
    #session = FuturesSession()
    session = Session()

    #request = session.get(url, params=payload)
    # #response = request.result()

    response = session.get(url, params=payload)


    if response.status_code != 200:
        raise Exception("Error while downloading map from Google Maps API.")

    img = Image.open(BytesIO(response.content))

    # Calculate bounding box
    bbox = BoundingBox.createFromCenterPoint(lat, lon, zoom, img.size)

    return Map(img, (lat, lon), zoom, bbox)
