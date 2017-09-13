
from googlestaticmaps.projection import lon_to_x, lat_to_y


class PointMarker(object):

    def __init__(self, point, radius=5, color="red"):
        self._lat = point[0]
        self._lon = point[1]
        self._radius = radius
        self._color = color

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        # Convert lat lon to pixel coordinates relative to the center pixel
        x = lon_to_x(self._lon, zoom) - lon_to_x(centerPoint[1], zoom) + imgSize[0] / 2
        y = lat_to_y(self._lat, zoom) - lat_to_y(centerPoint[0], zoom) + imgSize[1] / 2

        a = [(x-self._radius, y-self._radius), (x+self._radius, y+self._radius)]


        imgDraw.ellipse(a, outline=self._color)


class LineMarker(object):

    def __init__(self, points, lineWidth=3, color="red"):
        self._points = points
        self._lineWidth = lineWidth
        self._color = color

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        coords = []

        for (lat, lon) in self._points:

            x = lon_to_x(lon, zoom) - lon_to_x(centerPoint[1], zoom) + imgSize[0] / 2
            y = lat_to_y(lat, zoom) - lat_to_y(centerPoint[0], zoom) + imgSize[1] / 2

            coords.append((x, y))

        imgDraw.line(coords, width=self._lineWidth, fill=self._color)


class PolygonMarker(object):

    def __init__(self, pointLst, color="red"):
        self._points = pointLst
        self._color = color

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        polygonPoints = []

        for lat, lon in self._points:

            x = lon_to_x(lon, zoom) - lon_to_x(centerPoint[1], zoom) + imgSize[0] / 2
            y = lat_to_y(lat, zoom) - lat_to_y(centerPoint[0], zoom) + imgSize[1] / 2

            polygonPoints.append((x, y))

        imgDraw.polygon(polygonPoints, outline=self._color)


class ArrowMarker(object):

    def __init__(self, point, direction, size=50, color="orange"):
        from math import pi

        self._lat = point[0]
        self._lon = point[1]
        self._direction = direction
        self._size = size
        self._color = color

        self._radius = 5

    def draw(self, imgDraw, zoom, centerPoint, imgSize):
        from math import sin, cos, pi

        # Center point
        x = lon_to_x(self._lon, zoom) - lon_to_x(centerPoint[1], zoom) + imgSize[0] / 2
        y = lat_to_y(self._lat, zoom) - lat_to_y(centerPoint[0], zoom) + imgSize[1] / 2


        polygonPoints = []

        # Arrow head
        dx = 3. / 4. * float(self._size) * cos(self._direction)
        dy = 3. / 4. * float(self._size) * sin(self._direction)

        polygonPoints.append((x + dx, y - dy))

        # Left back
        dx = -1. / 2. * float(self._size) * cos(self._direction - pi/5)
        dy = -1. / 2. * float(self._size) * sin(self._direction - pi/5)

        polygonPoints.append((x + dx, y - dy))

        # Base
        dx = -1. / 4. * float(self._size) * cos(self._direction)
        dy = -1. / 4. * float(self._size) * sin(self._direction)

        polygonPoints.append((x + dx, y - dy))

        # Right back
        dx = -1. / 2. * float(self._size) * cos(self._direction + pi/5)
        dy = -1. / 2. * float(self._size) * sin(self._direction + pi/5)

        polygonPoints.append((x + dx, y - dy))

        imgDraw.polygon(polygonPoints, outline="black", fill=self._color)

        # White point in the middle
        r = max(3, self._size / 20)
        imgDraw.ellipse([(x-r, y-r), (x+r, y+r)], outline="black", fill=self._color)



