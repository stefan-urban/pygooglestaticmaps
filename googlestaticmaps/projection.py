"""
Helper functions to convert coordinates between three different systems:
 - Longitude/Latitude
 - WGS 84 (Web Mercator) as defined in https://epsg.io/3857
 - Google Maps static images, which is a transposed and scaled variation of WGS 84

Formulas based on Bing Maps Tile System, Map Projection Documentation:
 > https://msdn.microsoft.com/en-us/library/bb259689.aspx
"""

import math

EARTH_RADIUS = 6378137


def convert_lonlat_to_px(lon, lat, zoom, radians=False):

    if not radians:
        lon = math.radians(lon)
        lat = math.radians(lat)

    pixelX = (lon + math.pi) / (2 * math.pi) * (256 * pow(2, zoom))
    pixelY = 0.5 * (1 - math.log(math.tan(lat) + 1 / math.cos(lat)) / math.pi) * (pow(2, zoom) * 256)

    return int(round(pixelX)), int(round(pixelY))


def convert_px_to_lonlat(pixelX, pixelY, zoom, radians=False):

    lon = pixelX / (256 * pow(2, zoom)) * (2 * math.pi) - math.pi
    lat = (math.pi / 2) - 2 * math.atan(math.exp((2 * math.pi * pixelY) / (256*pow(2, zoom)) - math.pi))

    if not radians:
        lon = math.degrees(lon)
        lat = math.degrees(lat)

    return lon, lat


def convert_lonlat_to_merc(lon, lat, radians=False):
    if not radians:
        lon = math.radians(lon)
        lat = math.radians(lat)

    x = lon * EARTH_RADIUS
    y = math.log(math.tan(math.pi / 4 + lat / 2)) * EARTH_RADIUS

    return x, y


def convert_merc_to_lonlat(x, y, radians=False):

    lon = x / EARTH_RADIUS
    lat = math.atan(math.sinh(y / EARTH_RADIUS))

    if not radians:
        lon = math.degrees(lon)
        lat = math.degrees(lat)

    return lon, lat


def convert_merc_to_px(x, y, zoom):

    pixelX = (x + math.pi * EARTH_RADIUS) / (2 * math.pi * EARTH_RADIUS) * (256 * pow(2, zoom))
    pixelY = 0.5 * (1 - (y / (math.pi * EARTH_RADIUS))) * (256 * pow(2, zoom))

    return int(round(pixelX)), int(round(pixelY))


def convert_px_to_merc(pixelX, pixelY, zoom):

    x = pixelX / (256 * pow(2, zoom)) * (2 * math.pi * EARTH_RADIUS) - math.pi * EARTH_RADIUS
    y = (1 - pixelY / (256 * pow(2, zoom)) * 2) * (math.pi * EARTH_RADIUS)

    return x, y



if __name__ == '__main__':

    print("Doing tests:")

    data = [
        (3, 39.81447, -98.565388, 463, 777, -10972248.80, 4839018.08),
        (3, 40.609538, -80.224528, 568, 771, -8930553.61, 4954918.09),
        (10, 0.0, 0.0, 2**10*256/2, 2**10*256/2, 0.0, 0.0),
        (21, 11.645244, 48.268232, 340418261, 250947991, 5373195.007731592, 1305361.1794719186)
    ]

    def close(floats, floats2):
        assert abs(floats[0] - floats2[0]) < 1, (floats[0], floats2[0])
        assert abs(floats[1] - floats2[1]) < 1, (floats[1], floats2[1])
        return True

    def between(floats, floats1, floats2):
        assert floats1[0] <= floats[0] <= floats2[0]
        assert floats1[1] <= floats[1] <= floats2[1]
        return True

    for i, (zoom, lat, lng, pixelX, pixelY, x, y) in enumerate(data):
        print("#" + str(i))

        res = convert_lonlat_to_px(lng, lat, zoom)
        #print(res)
        if res == (pixelX, pixelY):
            print("... ok.")
        else:
            print("... not ok!")

        res = convert_px_to_lonlat(pixelX, pixelY, zoom)
        #print(res)
        if close(res, (lng, lat)):
            print("... ok.")
        else:
            print("... not ok!")

        res = convert_lonlat_to_merc(lng, lat)
        #print(res)
        if close(res, (x, y)):
            print("... ok.")
        else:
            print("... not ok!")

        res = convert_merc_to_lonlat(x, y)
        #print(res)
        if close(res, (lng, lat)):
            print("... ok.")
        else:
            print("... not ok!")

        res = convert_merc_to_px(x, y, zoom)
        #print(res)
        if res == (pixelX, pixelY):
            print("... ok.")
        else:
            print("... not ok!")
