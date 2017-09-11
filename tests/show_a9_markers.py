
from googlestaticmaps.provider import get_map_at_latlon
from googlestaticmaps.marker import PointMarker, LineMarker


road_markings = [
    {'from': (48.268336, 11.645252), 'to': (48.268284, 11.645271)},
    {'from': (48.268330, 11.645202), 'to': (48.268279, 11.645220)},
    {'from': (48.268167, 11.645209), 'to': (48.268115, 11.645227)},
]


with open("googlemaps_apikey.txt") as fh:
    apikey = fh.read()
    fh.close()

themap = get_map_at_latlon(48.268232, 11.645244, 21, (700, 700), apikey)

# Point markers
from googlestaticmaps.marker import PointMarker

for road_marking in road_markings:
    themap.addMarker(PointMarker(
        lat=road_marking['from'][0],
        lon=road_marking['from'][1],
        radius=4,
        color="red"),
        inhibitRender=True
    )
    themap.addMarker(PointMarker(
        lat=road_marking['to'][0],
        lon=road_marking['to'][1],
        radius=4,
        color="red"),
        inhibitRender=True
    )

# Line markers
for road_marking in road_markings:
    themap.addMarker(LineMarker(
        lat1=road_marking['from'][0],
        lon1=road_marking['from'][1],
        lat2=road_marking['to'][0],
        lon2=road_marking['to'][1],
        lineWidth=3,
        color="green"
    ), inhibitRender=True)


themap.render().show()
