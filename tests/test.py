
import pyproj
from googlestaticmaps import get_map_at_lonlat, convert_xy_to_ll, convert_wm_to_ll


gapikey = " AIzaSyAGumGLMszqlU-1oYN9KSYAiS-Gt6TXJrM "


x, y = (696999, 5356444)

print((x, y))

p1 = pyproj.Proj('+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')

lon, lat = p1(x, y, inverse=True)

print("{}N, {}E".format(lat, lon))
