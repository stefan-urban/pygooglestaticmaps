
import numpy as np

from googlestaticmaps.provider import get_map_at_latlon


# Get google maps apikey
try:
    with open("googlemaps_apikey.txt") as fh:
        googlemaps_apikey = fh.read()
        fh.close()
except IOError:
    print("No google maps apikey found!")
    quit(-1)


def precalculated(lat, lon, zoom, imgSize):

    expectedResult = [48.14272340433031, 11.21429443359375, 48.25714137039319, 11.385955810546875]
    result = get_map_at_latlon(lat, lon, zoom, imgSize, googlemaps_apikey).boundingBox.list

    if not np.allclose(result, expectedResult, rtol=1.e-4, atol=1.e-6):
        return False

    return True

def bingmaps(lat, lon, zoom, imgSize):
    """ Bing uses the same projection and zoom levels and returns the bbox as meta data """

    from requests_futures.sessions import FuturesSession
    from PIL import Image
    from io import StringIO, BytesIO

    # Get api key
    try:
        with open("bingmaps_apikey.txt") as fh:
            apikey = fh.read()
            fh.close()
    except IOError:
        return False

    # Build URL
    url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/"
    url += str(lat) + "," + str(lon) + "/" + str(zoom)

    payload = {
        'mapSize': ",".join(str(x) for x in imgSize),
        'mapLayer': '',
        'mapMetadata': '1',
        'key': apikey
    }

    session = FuturesSession()
    request = session.get(url, params=payload)

    response = request.result()

    if response.status_code != 200:

        if response.status_code == 401:
            print("Bing Maps returned 401 error, api key was not accepted?")
            return False

        return False

    json_data = response.json()

    expectedResult = [float(x) for x in json_data['resourceSets'][0]['resources'][0]['bbox']]
    result = get_map_at_latlon(lat, lon, zoom, imgSize, googlemaps_apikey).boundingBox.list

    if not np.allclose(result, expectedResult, rtol=1.e-4, atol=1.e-8):
        return False

    return True


if __name__ == "__main__":
    lat = 48.2
    lon = 11.3
    zoom = 12
    imgSize = (500, 500)


    tests = {
        "Precalculated results": precalculated,
        "Bing Maps API": bingmaps
    }

    check = True

    for testName, test in tests.items():

        if test(lat, lon, zoom, imgSize) is False:
            check = False
            print("Test \"" + str(testName) + "\" failed!")
        else:
            print("Test \"" + str(testName) + "\" was OK!")

    print("----")
    if check:
        print("All tests passed!")
    else:
        print("One or more error occurred!")
