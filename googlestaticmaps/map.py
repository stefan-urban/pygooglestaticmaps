
from PIL import ImageDraw


class Map(object):

    def __init__(self, mapImage, centerPoint, zoom, boundingBox):
        self._mapImage = mapImage
        self._centerPoint = centerPoint
        self._zoom = zoom
        self._boundingBox = boundingBox

        self._renderedMapImage = None

        self._markers = []

    @property
    def mapImage(self):
        return self._mapImage

    @property
    def renderedMapImage(self):
        if self._renderedMapImage is None:
            return self._mapImage

        return self._renderedMapImage

    @property
    def centerPoint(self):
        return self._centerPoint

    @property
    def boundingBox(self):
        return self._boundingBox

    def addMarker(self, marker, inhibitRender=False):
        """ Adds marker to list and updates rendered image (can be inhibited) """

        self._markers.append(marker)

        if inhibitRender is False:
            self.render()

    def render(self):
        """ Draws all markers """
        self._renderedMapImage = self._mapImage

        draw = ImageDraw.Draw(self._renderedMapImage)

        for marker in self._markers:
            marker.draw(draw, self._zoom, self._centerPoint, self._renderedMapImage.size)

        del draw

        return self._renderedMapImage
