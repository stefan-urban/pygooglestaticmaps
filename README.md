
Google Maps Static Images
=========================

## Information

This library lets you download an image from the Google Maps API. It provides additional meta information as well as a few drawing functions.

You need a Google Maps API key. Put it in a file called ```googlemaps_apikey.txt```.

## Limitations

The Google Maps API provides images that are a few centimeters off. The reason is unknown.

lat += 0.0
lon += 0.000005

## Installation

```bash
pip install https://github.com/stefan-urban/pygooglestaticmaps/archive/master.zip
```

## Examples

Show part of the german Autobahn A9.

```python
from googlestaticmaps.provider import get_map_at_latlon

themap = get_map_at_latlon(lat=48.268232, lon=11.645244, zoom=21, imgSize=(700, 700), apikey="123456")

themap.mapImage.show()
```

Addionally you can create markers on the map, based on lat/lon data:

```python
from googlestaticmaps.marker import PointMarker

road_markings = [
    {'from': (48.268336, 11.645252), 'to': (48.268284, 11.645271)},
    {'from': (48.268330, 11.645202), 'to': (48.268279, 11.645220)},
    {'from': (48.268167, 11.645209), 'to': (48.268115, 11.645227)},
]

# Point markers
for road_marking in road_markings:
    themap.addMarker(PointMarker(
        lat=road_marking['from'][0],
        lon=road_marking['from'][1],
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
```
