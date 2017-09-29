
from scipy.spatial import distance

from googlestaticmaps.projection import convert_ll_to_px, convert_ll_to_xy, convert_ll_to_xy, convert_xy_to_px, convert_px_to_ll, convert_px_to_xy


# Test 1: Distance is between 59 and 61 pixels at zoom level 19

lat1, lon1 = (48.414847, 10.871933)
lat2, lon2 = (48.414844, 10.872093)

result1 = convert_ll_to_px(lon1, lat1, 19)
result2 = convert_ll_to_px(lon2, lat2, 19)

assert 59 <= distance.euclidean(result1, result2) <= 61

lon1a, lat1a = convert_px_to_ll(result1[0], result1[1], 19)
lon2a, lat2a = convert_px_to_ll(result2[0], result2[1], 19)

assert abs(lon1 - lon1a) < 1e-5
assert abs(lat1 - lat1a) < 1e-5
assert abs(lon2 - lon2a) < 1e-5
assert abs(lat2 - lat2a) < 1e-5


# Test 2: Distance is between at zoom level 20

lat1, lon1 = (48.414847, 10.871933)
lat2, lon2 = (48.414844, 10.872093)

result = distance.euclidean(convert_ll_to_px(lon1, lat1, 20), convert_ll_to_px(lon2, lat2, 20))

assert 119 <= result <= 121


# Test 3: Center of the world

x, y = convert_xy_to_px(128, 128, 0)

assert abs(x - 128) < 1e-10
assert abs(y - 128) < 1e-10

x, y = convert_px_to_xy(128, 128, 0)

assert abs(x - 128) < 1e-4
assert abs(y - 128) < 1e-4


print("All tests passed!")
