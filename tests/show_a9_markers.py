
from googlestaticmaps import get_map_at_lonlat, PointMarker, PolygonMarker, CarMarker, ArrowMarker, LineMarker


with open("googlemaps_apikey.txt") as fh:
    gapikey = fh.read()
    fh.close()


poi = (11.645244, 48.268232)

road_markings = [
    {'from': (11.645252, 48.268336), 'to': (11.645271, 48.268284)},
    {'from': (11.645202, 48.268330), 'to': (11.645220, 48.268279)},
    {'from': (11.645209, 48.268167), 'to': (11.645227, 48.268115)},
]

road_polygon = [
    (11.645256, 48.268173),
    (11.645274, 48.268120),
    (11.645323, 48.268127),
    (11.645305, 48.268180)
]

diff = 0.00002
road_polygon_overlap = [(lon + diff, lat + diff) for lon, lat in road_polygon]

car = {
    'pos': (11.645237, 48.268307),
    'width': 17 / 12 * 2.0,
    'length': 17 / 12 * 4.2,
    'heading': 1.8
}


themap = get_map_at_lonlat(poi[0], poi[1], 21, imgSize=(700, 700), apikey=gapikey)

# Point markers
for road_marking in road_markings:
    themap.addMarker(PointMarker(
        point=road_marking['from'],
        radius=4,
        outline="red"
        ), inhibitRender=True)
    themap.addMarker(PointMarker(
        point=road_marking['to'],
        radius=4,
        outline="red"
        ), inhibitRender=True)

# Car markers
themap.addMarker(CarMarker(
    point=car['pos'],
    width=car['width'],
    length=car['length'],
    heading=car['heading'],
    color="red"
    ), inhibitRender=True)

# Line markers
for road_marking in road_markings:
    themap.addMarker(LineMarker(
        points=[road_marking['from'], road_marking['to']],
        lineWidth=3,
        color="green"
    ), inhibitRender=True)

themap.addMarker(LineMarker(
    points=[
        (11.645303, 48.268344),
        (11.645374, 48.268135)
    ],
    lineWidth=1,
    color="red",
    markerColor="green"
))

# Polygon marker
themap.addMarker(PolygonMarker(
    pointLst=road_polygon,
    outline="green",
    fill=(0, 255, 0, 60)
), inhibitRender=True)

themap.addMarker(PolygonMarker(
    pointLst=road_polygon_overlap,
    outline="red",
    fill=(255, 0, 0, 60)
), inhibitRender=True)

# Arrow marker
themap.addMarker(ArrowMarker(
    point=poi,
    heading=1.9,
    size=10
), inhibitRender=True)


themap.render().show()
