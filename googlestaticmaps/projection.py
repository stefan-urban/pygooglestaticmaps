
from math import radians, degrees, pi
from math import cos, tan, sinh, atan, log

import numpy as np


def lon_to_x(lon, zoom):
    lonrad = radians(lon)

    # Limit longitude to [-2pi, 2pi]
    if not -2 * pi <= lon <= 2 * pi:
        lonrad = (lonrad + pi) % (2 * pi) - pi

    return ((lonrad + pi) / (2 * pi)) * pow(2, zoom) * 256

def lat_to_y(lat, zoom):
    latrad = radians(lat)

    # Limit latitude to [-pi, pi]
    if not pi / -2 <= latrad <= pi / 2:
        latrad = (latrad + pi / 2) % pi - pi / 2

    # https://de.wikipedia.org/wiki/Mercator-Projektion#Abbildungsgleichungen_f.C3.BCr_normale_Lage
    merc_y = log(tan(latrad) + 1 / cos(latrad))

    # Scale to pixels
    # TODO clarify why!
    return 0.5 * (1 - merc_y / pi) * pow(2, zoom) * 256

def x_to_lon(x, zoom):
    xrad = x / 256 / pow(2, zoom) * (2 * pi) - pi
    return degrees(xrad)

def y_to_lat(y, zoom):
    # Scale back from pixels to mercator y
    # TODO clarify why!
    merc_y = pi * (1 - 2 * y / 256 / pow(2, zoom))

    # https://de.wikipedia.org/wiki/Mercator-Projektion#Abbildungsgleichungen_f.C3.BCr_normale_Lage
    lat = atan(sinh(merc_y))

    return degrees(lat)

def latlon_to_xy(lat, lon, zoom):
    return np.array([lon_to_x(lon, zoom), lat_to_y(lat, zoom)])

def xy_to_latlon(x, y, zoom):
    return np.array([y_to_lat(y, zoom), x_to_lon(x, zoom)])
