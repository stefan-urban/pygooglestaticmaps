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


# Using pyproj for WGS84/UTM 32N projection
# Source: example https://epsg.io/32632
def _ll_to_zone_number(lon, lat):
    if 3.0 <= lon < 12 and 56.0 <= lat < 64:
        return 32
    
    if lon >= 0 and 72 <= lat <= 84:
        if lon <9:
            return 31
        elif lon < 21:
            return 33
        elif lon < 33:
            return 35
        elif lon < 42:
            return 37
        
    return (int((lon + 180)  / 6) + 1) % 60

def _lat_to_zone_letter(lat):
    if not -80 <= lat <= 84:
        raise Exception()
    
    return "CDEFGHJKLMNPQRSTUVWXX"[int(lat + 80) >> 3]

def convert_ll_to_utm(lon, lat, radians=False):
    zone = str(_ll_to_zone_number(lon, lat)) + _lat_to_zone_letter(lat)
    
    proj = pyproj.Proj("+proj=utm +zone={:s} +datum=WGS84 +units=m +no_defs".format(zone))
    
    x, y = proj(lon, lat, radians=radians)
    
    return x, y, zone
    
def convert_utm_to_ll(x, y, zone, radians=False):
    
    proj = pyproj.Proj("+proj=utm +zone={:s} +datum=WGS84 +units=m +no_defs".format(zone))
    
    return proj(x, y, inverse=True, radians=radians)


# Using pyproj for web mercator projection
# Source: http://spatialreference.org/ref/sr-org/7483/
#      or https://epsg.io/3857
_proj_wm = pyproj.Proj("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs")

# Maximum latitude (https://en.wikipedia.org/wiki/Mercator_projection#Truncation_and_aspect_ratio)
lat_max = math.atan(math.sinh(math.pi))

# Calculate outer limits of projection
x_wm_min, y_wm_min = _proj_wm(-180.0, math.degrees(-lat_max), radians=False)
x_wm_max, y_wm_max = _proj_wm(+180.0, math.degrees(+lat_max), radians=False)

x_wm_offset = abs(x_wm_min)
y_wm_offset = abs(y_wm_min)

x_wm_abs = abs(x_wm_min) + abs(x_wm_max)
y_wm_abs = abs(y_wm_min) + abs(y_wm_max)


def convert_ll_to_wm(lon, lat, radians=False):
    return _proj_wm(lon, lat, radians=radians)

def convert_wm_to_ll(mx, my, radians=False):
    return _proj_wm(mx, my, inverse=True, radians=radians)

def convert_ll_to_xy(lon, lat, radians=False):
    mx, my = convert_ll_to_wm(lon, lat, radians=radians)

    # Convert to Google world coordinates
    gx = (mx + x_wm_offset) / x_wm_abs * 256.0
    gy = (1 - (my + y_wm_offset) / y_wm_abs) * 256.0

    return gx, gy

def convert_xy_to_ll(gx, gy, radians=False):

    # Convert to web mercator
    mx = (gx / 256.0 * x_wm_abs) - x_wm_offset
    my = (1 - gy / 256.0) * y_wm_abs - y_wm_offset

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
