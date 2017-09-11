
from googlestaticmaps.projection import lon_to_x, lat_to_y


class PointMarker(object):

    def __init__(self, lat, lon, radius=5, color="red"):
        self._radius = radius
        self._color = color
        self._lat = lat
        self._lon = lon

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        # Convert lat lon to pixel coordinates relative to the center pixel
        pX = lon_to_x(self._lon, zoom) - lon_to_x(centerPoint[1], zoom) + imgSize[0] / 2
        pY = lat_to_y(self._lat, zoom) - lat_to_y(centerPoint[0], zoom) + imgSize[1] / 2

        a = [(pX-self._radius, pY-self._radius), (pX+self._radius, pY+self._radius)]

        imgDraw.ellipse(a, outline=self._color)


class LineMarker(object):

    def __init__(self, lat1, lon1, lat2, lon2, lineWidth=3, color="red"):
        self._lineWidth = lineWidth
        self._color = color
        self._lat1 = lat1
        self._lon1 = lon1
        self._lat2 = lat2
        self._lon2 = lon2

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        x1 = lon_to_x(self._lon1, zoom) - lon_to_x(centerPoint[1], zoom) + imgSize[0] / 2
        y1 = lat_to_y(self._lat1, zoom) - lat_to_y(centerPoint[0], zoom) + imgSize[1] / 2

        x2 = lon_to_x(self._lon2, zoom) - lon_to_x(centerPoint[1], zoom) + imgSize[0] / 2
        y2 = lat_to_y(self._lat2, zoom) - lat_to_y(centerPoint[0], zoom) + imgSize[1] / 2

        imgDraw.line([(x1, y1), (x2, y2)], width=self._lineWidth, fill=self._color)
