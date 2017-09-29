"""
Helper functions to convert coordinates between three different systems:
 - ll: Longitude/Latitude (WGS 84)
 - wm : Web mercator projected coordinates (unit: meters!)
 - xy : Google Maps world coordinates
 - px : Google Maps pixel coordinates based on zoom level

The projection WGS 84 (lonlat) to World Coordinates (xy) is called "Mercator projection". They are
then scaled to a coordinate system that ranges from 0.0 to 256.0 on both axis.
"""

import math
import pyproj


# Using pyproj for projection
# Source: http://spatialreference.org/ref/sr-org/7483/
#      or https://epsg.io/3857
_proj = pyproj.Proj("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs")

# lonlat > xy: _proj(lon, lat)
# xy > lonlat: _proj(x, y)

# Maximum latitude (https://en.wikipedia.org/wiki/Mercator_projection#Truncation_and_aspect_ratio)
lat_max = math.atan(math.sinh(math.pi))

# Calculate outer limits of projection
x_merc_min, y_merc_min = _proj(-180.0, math.degrees(-lat_max), radians=False)
x_merc_max, y_merc_max = _proj(+180.0, math.degrees(+lat_max), radians=False)

x_merc_offset = abs(x_merc_min)
y_merc_offset = abs(y_merc_min)

x_merc_abs = abs(x_merc_min) + abs(x_merc_max)
y_merc_abs = abs(y_merc_min) + abs(y_merc_max)


def convert_ll_to_wm(lon, lat, radians=False):
    return _proj(lon, lat, radians=radians)

def convert_wm_to_ll(mx, my, radians=False):
    return _proj(mx, my, inverse=True, radians=radians)

def convert_ll_to_xy(lon, lat, radians=False):
    mx, my = convert_ll_to_wm(lon, lat, radians=radians)

    # Convert to Google world coordinates
    gx = (mx + x_merc_offset) / x_merc_abs * 256.0
    gy = (1 - (my + y_merc_offset) / y_merc_abs) * 256.0

    return gx, gy

def convert_xy_to_ll(gx, gy, radians=False):

    # Convert to web mercator
    mx = (gx / 256.0 * x_merc_abs) - x_merc_offset
    my = (1 - gy / 256.0) * y_merc_abs - y_merc_offset

    return convert_wm_to_ll(mx, my, radians=radians)

def convert_xy_to_px(gx, gy, zoom):
    px = gx * pow(2, zoom)
    py = gy * pow(2, zoom)
    return int(round(px)), int(round(py))

def convert_px_to_xy(px, py, zoom):
    return px / pow(2, zoom), py / pow(2, zoom)

def convert_ll_to_px(lon, lat, zoom, radians=False):
    gx, gy = convert_ll_to_xy(lon, lat, radians=radians)
    return convert_xy_to_px(gx, gy, zoom)

def convert_px_to_ll(px, py, zoom, radians=False):
    gx, gy = convert_px_to_xy(px, py, zoom)
    return convert_xy_to_ll(gx, gy, radians=radians)


if __name__ == '__main__':

    print("Doing tests:")

    # [zoom, lon, lat, pixelX, pixelY, googleX, googleY]
    data = [
        (0, -180.0, 0.0, 0, 128, 0.0, 128.0),
        (4, +180.0, 0.0, 256*pow(2, 4), 128*pow(2, 4), 256.0, 128.0),
        (3, -87.64999999999998, 41.85, 525, 761, 65.67111111111113, 95.17492654697409), # Directly from Google's examples
        (15, 11.638754000000063, 48.285702, 4465506, 2906024, 136.27644728888893, 88.68481866002884),
        (11, 19.084753999999975, 74.441957, 289938, 96040, 141.5713806222222, 46.89462533935128),
    ]

    def close(floats, floats2):
        assert abs(floats[0] - floats2[0]) <= 1, (floats[0], floats2[0])
        assert abs(floats[1] - floats2[1]) <= 1, (floats[1], floats2[1])
        return True

    def between(floats, floats1, floats2):
        assert floats1[0] <= floats[0] <= floats2[0]
        assert floats1[1] <= floats[1] <= floats2[1]
        return True

    for i, (zoom, lon, lat, pixelX, pixelY, x, y) in enumerate(data):
        print("#" + str(i))

        res = convert_ll_to_xy(lon, lat)
        #print(res)
        #print((x, y))
        if close(res, (x, y)):
            print("... ok.")
        else:
            print("... not ok!")

        res = convert_xy_to_ll(x, y)
        #print(res)
        if close(res, (lon, lat)):
            print("... ok.")
        else:
            print("... not ok!")

        res = convert_xy_to_px(x, y, zoom)
        #print(res)
        #print((pixelX, pixelY))
        if close(res, (pixelX, pixelY)):
            print("... ok.")
        else:
            print("... not ok!")

        res = convert_ll_to_px(lon, lat, zoom)
        #print(res)
        #print((pixelX, pixelY))
        if close(res, (pixelX, pixelY)):
            print("... ok.")
        else:
            print("... not ok!")

        res = convert_px_to_ll(pixelX, pixelY, zoom)
        #print(res)
        if close(res, (lon, lat)):
            print("... ok.")
        else:
            print("... not ok!")

    print("All tests passed!")