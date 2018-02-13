from googlestaticmaps.projection import *


print("Doing tests:")

# [zoom, lon, lat, pixelX, pixelY, googleX, googleY, utmx, utmy, utmzone]
data = [
    (0, -180.0, 0.0, 0, 128, 0.0, 128.0, 166021.44, 0.0, "1N"),
    (4, +180.0, 0.0, 256*pow(2, 4), 128*pow(2, 4), 256.0, 128.0, 166021.44, 0.0, "1N"),
    (3, -87.64999999999998, 41.85, 525, 761, 65.67111111111113, 95.17492654697409, 446042.18, 4633326.32, "16T"), # Directly from Google's examples
    (15, 11.638754000000063, 48.285702, 4465506, 2906024, 136.27644728888893, 88.68481866002884, 695742.05, 5351421.42, "32U"),
    (11, 19.084753999999975, 74.441957, 289938, 96040, 141.5713806222222, 46.89462533935128, 622203.52, 8265543.94, "33X"),
]

def close(floats, floats2):
    assert abs(floats[0] - floats2[0]) <= 1, (floats[0], floats2[0])
    assert abs(floats[1] - floats2[1]) <= 1, (floats[1], floats2[1])
    return True

def between(floats, floats1, floats2):
    assert floats1[0] <= floats[0] <= floats2[0]
    assert floats1[1] <= floats[1] <= floats2[1]
    return True

for i, (zoom, lon, lat, pixelX, pixelY, x, y, utmx, utmy, utmzone) in enumerate(data):
    print("#" + str(i))

    res = convert_ll_to_xy(lon, lat)
    #print(res)
    #print((x, y))
    if close(res, (x, y)):
        print("... ok.")
    else:
        print("... not ok!")

    res = convert_xy_to_ll(x, y)
    #print(res)
    if close(res, (lon, lat)):
        print("... ok.")
    else:
        print("... not ok!")

    res = convert_xy_to_px(x, y, zoom)
    #print(res)
    #print((pixelX, pixelY))
    if close(res, (pixelX, pixelY)):
        print("... ok.")
    else:
        print("... not ok!")

    res = convert_ll_to_px(lon, lat, zoom)
    #print(res)
    #print((pixelX, pixelY))
    if close(res, (pixelX, pixelY)):
        print("... ok.")
    else:
        print("... not ok!")

    res = convert_px_to_ll(pixelX, pixelY, zoom)
    #print(res)
    if close(res, (lon, lat)):
        print("... ok.")
    else:
        print("... not ok!")
        
    res = convert_ll_to_utm(lon, lat)
    #print(res)
    if close(res[0:2], (utmx, utmy)) and res[2] == utmzone:
        print("... ok.")
    else:
        print("... not ok!")

    
print("All tests passed!")
