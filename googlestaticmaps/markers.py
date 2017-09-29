
import math

from googlestaticmaps.projection import convert_ll_to_px, convert_ll_to_wm, convert_wm_to_ll


class PointMarker(object):

    def __init__(self, point, radius=5, fill=None, outline="red"):
        self._lon = point[0]
        self._lat = point[1]
        self._radius = radius
        self._fill = fill
        self._outline = outline

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        X, Y = convert_ll_to_px(self._lon, self._lat, zoom)
        cX, cY = convert_ll_to_px(centerPoint[0], centerPoint[1], zoom)

        x = X - cX + imgSize[0] / 2
        y = Y - cY + imgSize[1] / 2

        a = [
            (x - self._radius, y - self._radius),
            (x + self._radius, y + self._radius)
        ]

        imgDraw.ellipse(a, fill=self._fill, outline=self._outline)


class PolygonMarker(object):

    def __init__(self, pointLst, fill=None, outline="red"):
        self._points = pointLst
        self._fill = fill
        self._outline = outline

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        polygonPoints = []

        for lon, lat in self._points:

            X, Y = convert_ll_to_px(lon, lat, zoom)
            cX, cY = convert_ll_to_px(centerPoint[0], centerPoint[1], zoom)

            x = X - cX + imgSize[0] / 2
            y = Y - cY + imgSize[1] / 2

            polygonPoints.append((x, y))

        imgDraw.polygon(polygonPoints, fill=self._fill, outline=self._outline)


class ArrowMarker(object):

    def __init__(self, point, heading, size=50, fill=None, outline="red"):

        self._lon = point[0]
        self._lat = point[1]
        self._hdg = heading
        self._size = size
        self._fill = fill
        self._outline = outline

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        alpha = math.radians(40)

        merc_cX, merc_cY = convert_ll_to_wm(self._lon, self._lat)

        distances = [0.6 * self._size, 0.6 * self._size, 0.3 * self._size, 0.6 * self._size]
        angles = [self._hdg, self._hdg + math.pi - alpha, self._hdg + math.pi, self._hdg + math.pi + alpha]

        polygonPoints = []

        for distance, angle in zip(distances, angles):
            merc_x = merc_cX + distance * math.cos(angle)
            merc_y = merc_cY + distance * math.sin(angle)

            lon, lat = convert_wm_to_ll(merc_x, merc_y)

            polygonPoints.append((lon, lat))

        PolygonMarker(polygonPoints, fill=self._fill, outline=self._outline).draw(imgDraw, zoom, centerPoint, imgSize)


class CarMarker(object):

    def __init__(self, point, width, length, heading, color="blue"):
        self._point = point
        self._width = width
        self._length = length
        self._hdg = heading
        self._color = color

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        merc_cX, merc_cY = convert_ll_to_wm(self._point[0], self._point[1])

        # Draw outer box
        distance = 0.5 * math.hypot(self._width, self._length)
        alpha = math.atan(self._width / self._length)

        polygonPoints = []

        angles = [self._hdg + alpha, self._hdg - alpha, self._hdg + math.pi + alpha, self._hdg + math.pi - alpha]

        for angle in angles:
            merc_x = merc_cX + distance * math.cos(angle)
            merc_y = merc_cY + distance * math.sin(angle)

            lon, lat = convert_wm_to_ll(merc_x, merc_y)

            polygonPoints.append((lon, lat))

        PolygonMarker(polygonPoints, fill=self._color).draw(imgDraw, zoom, centerPoint, imgSize)
        ArrowMarker(self._point, self._hdg, self._width, fill="orange", outline=None).draw(imgDraw, zoom, centerPoint, imgSize)


class LineMarker(object):

    def __init__(self, points, lineWidth=3, color="red", markerColor=None):
        self._points = points
        self._lineWidth = lineWidth
        self._color = color
        self._markerColor = markerColor

    def draw(self, imgDraw, zoom, centerPoint, imgSize):

        if self._markerColor:

            for (lon, lat) in self._points:
                PointMarker((lon, lat), radius=self._lineWidth*3, fill=self._color, outline=self._markerColor).draw(imgDraw, zoom, centerPoint, imgSize)

        cX, cY = convert_ll_to_px(centerPoint[0], centerPoint[1], zoom)

        coords = []

        for (lon, lat) in self._points:

            X, Y = convert_ll_to_px(lon, lat, zoom)

            x = X - cX + imgSize[0] / 2
            y = Y - cY + imgSize[1] / 2

            coords.append((x, y))

        imgDraw.line(coords, width=self._lineWidth, fill=self._color)

