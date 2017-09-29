
import numpy as np

from googlestaticmaps.projection import convert_ll_to_px, convert_px_to_ll


class BoundingBox(object):

    @staticmethod
    def createFromCenterPointLonLat(lon, lat, zoom, imSize):

        # Convert to pixel coordinates
        center_x, center_y = convert_ll_to_px(lon, lat, zoom)

        westLon, northLat = convert_px_to_ll(center_x - imSize[0]/2., center_y - imSize[1]/2., zoom)
        eastLon, southLat = convert_px_to_ll(center_x + imSize[0]/2., center_y + imSize[1]/2., zoom)

        return BoundingBox(southLat, westLon, northLat, eastLon)


    def __init__(self, southLat, westLon, northLat, eastLon):
        self._southLat = southLat
        self._westLon = westLon
        self._northLat = northLat
        self._eastLon = eastLon

    @property
    def list(self):
        return [self._southLat, self._westLon, self._northLat, self._eastLon]

    def __str__(self):
        return str(self.list)

    def contains(self, lon, lat):
        if not self._southLat <= lat <= self._northLat:
            return False

        if not self._westLon <= lon <= self._eastLon:
            return False

        return True

if __name__ == '__main__':

    lat, lon = (48.311163096995415, 11.624248231357791)

    bbox = BoundingBox.createFromCenterPointLonLat(lon, lat, 19, (512, 512))

    print(bbox)
