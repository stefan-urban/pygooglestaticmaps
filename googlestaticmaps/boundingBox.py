
import numpy as np

from googlestaticmaps.projection import latlon_to_xy, xy_to_latlon


class BoundingBox(object):

    @staticmethod
    def createFromCenterPoint(lat, lon, zoom, imgSize):

        centerX, centerY = latlon_to_xy(lat, lon, zoom)

        swPixelX = centerX  - (imgSize[0] / 2)
        swPixelY = centerY + (imgSize[1] / 2)
        swLatLon = xy_to_latlon(swPixelX, swPixelY, zoom)

        nePixelX = centerX + (imgSize[0] / 2)
        nePixelY = centerY - (imgSize[1] / 2)
        neLatLon = xy_to_latlon(nePixelX, nePixelY, zoom)

        return BoundingBox(swLatLon[0], swLatLon[1], neLatLon[0], neLatLon[1])

    def __init__(self, southLat, westLon, northLat, eastLon):
        self._southLat = southLat
        self._westLon = westLon
        self._northLat = northLat
        self._eastLon = eastLon

    @property
    def southLat(self):
        return self._southLat

    @property
    def westLon(self):
        return self._westLon

    @property
    def northLat(self):
        return self._northLat

    @property
    def eastLon(self):
        return self._eastLon

    @property
    def corners(self):
        return [
            (self._southLat, self._westLon),
            (self._northLat, self._westLon),
            (self._northLat, self._eastLon),
            (self._southLat, self._eastLon)
        ]

    @property
    def swCorner(self):
        return (self._southLat, self._westLon)

    @property
    def nwCorner(self):
        return (self._northLat, self._westLon)

    @property
    def neCorner(self):
        return (self._northLat, self._eastLon)

    @property
    def seCorner(self):
        return (self._southLat, self._eastLon)

    @property
    def list(self):
        return np.array([self._southLat, self._westLon, self._northLat, self._eastLon])

    @property
    def contains(self, lat, lon):
        if not self._southLat <= lat <= self._northLat:
            return False

        if not self._westLon <= lon <= self._eastLon:
            return False

        return True
