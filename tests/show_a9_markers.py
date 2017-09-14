
from googlestaticmaps.provider import get_map_at_latlon
from googlestaticmaps.marker import PointMarker, LineMarker, PolygonMarker, ArrowMarker


# Get google maps apikey
try:
    with open("googlemaps_apikey.txt") as fh:
        googlemaps_apikey = fh.read()
        fh.close()
except IOError:
    print("No google maps apikey found!")
    quit(-1)


poi = (48.268232, 11.645244)

road_markings = [
    {'from': (48.268336, 11.645252), 'to': (48.268284, 11.645271)},
    {'from': (48.268330, 11.645202), 'to': (48.268279, 11.645220)},
    {'from': (48.268167, 11.645209), 'to': (48.268115, 11.645227)},
]

road_polygon = [
    (48.268173, 11.645256),
    (48.268120, 11.645274),
    (48.268127, 11.645323),
    (48.268180, 11.645305)
]


themap = get_map_at_latlon(poi[0], poi[1], 21, (700, 700), googlemaps_apikey)

# Point markers
for road_marking in road_markings:
    themap.addMarker(PointMarker(
        point=road_marking['from'],
        radius=4,
        color="red"
        ), inhibitRender=True)
    themap.addMarker(PointMarker(
        point=road_marking['to'],
        radius=4,
        color="red"
        ), inhibitRender=True)

# Line markers
for road_marking in road_markings:
    themap.addMarker(LineMarker(
        points=[road_marking['from'], road_marking['to']],
        lineWidth=3,
        color="green"
    ), inhibitRender=True)

# Polygon marker
themap.addMarker(PolygonMarker(
    pointLst=road_polygon,
    color="white"
), inhibitRender=True)

# Arrow marker
themap.addMarker(ArrowMarker(
    point=poi,
    direction=1.9,
    size=100
), inhibitRender=True)


themap.render().show()
