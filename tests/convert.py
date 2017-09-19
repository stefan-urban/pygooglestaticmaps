
from scipy.spatial import distance

from googlestaticmaps.projection import convert_lonlat_to_px, convert_lonlat_to_merc, convert_merc_to_lonlat, convert_merc_to_px, convert_px_to_lonlat, convert_px_to_merc


# Test 1: Distance is between 59 and 61 pixels at zoom level 19

lat1, lon1 = (48.414847, 10.871933)
lat2, lon2 = (48.414844, 10.872093)

result1 = convert_lonlat_to_px(lon1, lat1, 19)
result2 = convert_lonlat_to_px(lon2, lat2, 19)

assert 59 <= distance.euclidean(result1, result2) <= 61

lon1a, lat1a = convert_px_to_lonlat(result1[0], result1[1], 19)
lon2a, lat2a = convert_px_to_lonlat(result2[0], result2[1], 19)

assert abs(lon1 - lon1a) < 1e-5
assert abs(lat1 - lat1a) < 1e-5
assert abs(lon2 - lon2a) < 1e-5
assert abs(lat2 - lat2a) < 1e-5


# Test 2: Distance is between at zoom level 20

lat1, lon1 = (48.414847, 10.871933)
lat2, lon2 = (48.414844, 10.872093)

result = distance.euclidean(convert_lonlat_to_px(lon1, lat1, 20), convert_lonlat_to_px(lon2, lat2, 20))

assert 119 <= result <= 121


# Test 3: Random point in Australia

lon, lat = (118.828125, -30.7512778)

result_x, result_y = convert_lonlat_to_merc(lon, lat)

assert abs(result_x - 13227886.366919) < 1e-4
assert abs(result_y - -3600489.783455) < 1e-4

lona, lata = convert_merc_to_lonlat(result_x, result_y)

assert abs(lon - lona) < 1e-5
assert abs(lat - lata) < 1e-5


# Test 4: Center of the world

x, y = convert_merc_to_px(0, 0, 0)

assert abs(x - 128) < 1e-10
assert abs(y - 128) < 1e-10

x, y = convert_px_to_merc(128, 128, 0)

assert abs(x) < 1e-4
assert abs(y) < 1e-4


print("All tests passed!")
