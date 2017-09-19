"""
Helper functions to convert coordinates between three different systems:
 - Longitude/Latitude
 - WGS 84 (Web Mercator) as defined in https://epsg.io/3857
 - Google Maps static images, which is a transposed and scaled variation of WGS 84

"""

from pyproj import Proj
import numpy as np

# Contant values are taken from: https://epsg.io/3857
_projection = Proj("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs")

# World dimensions
_x_0, _y_0 = _projection(-180.0, -85.06, radians=False)
_x_1, _y_1 = _projection(+180.0, +85.06, radians=False)


def convert_lonlat_to_px(lon, lat, zoom, radians=False):

    merc_x, merc_y = convert_lonlat_to_merc(lon, lat, radians=radians)
    return convert_merc_to_px(merc_x, merc_y, zoom)


def convert_px_to_lonlat(x, y, zoom, radians=False):

    # Convert lists to numpy arrays
    if isinstance(x, list) or isinstance(y, list):
        x = np.array(x)
        y = np.array(y)

    merc_x, merc_y = convert_px_to_merc(x, y, zoom)
    return _projection(merc_x, merc_y, radians=radians, inverse=True)


def convert_lonlat_to_merc(lon, lat, radians=False):

    # Convert lists to numpy arrays
    if isinstance(lon, list) or isinstance(lat, list):
        lon = np.array(lon)
        lat = np.array(lat)

    return _projection(lon, lat, radians=radians)


def convert_merc_to_lonlat(x, y, radians=False):

    # Convert lists to numpy arrays
    if isinstance(x, list) or isinstance(y, list):
        x = np.array(x)
        y = np.array(y)

    return _projection(x, y, radians=radians, inverse=True)


def convert_merc_to_px(x, y, zoom):
    x = (x - _x_0) * (256.0 * pow(2, zoom) / (_x_1 - _x_0))
    y = (y - _y_0) * (256.0 * pow(2, zoom) / (_y_1 - _y_0))

    return x, y


def convert_px_to_merc(x, y, zoom):
    x = x / (256.0 * pow(2, zoom) / (_x_1 - _x_0)) + _x_0
    y = y / (256.0 * pow(2, zoom) / (_y_1 - _y_0)) + _y_0

    return x, y
