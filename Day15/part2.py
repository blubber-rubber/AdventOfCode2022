import time
import re
from shapely.geometry import Polygon
from shapely.ops import unary_union
import numpy as np

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

formatting = "^Sensor at x=([\-0-9]*), y=([\-0-9]*): closest beacon is at x=([\-0-9]*), y=([\-0-9]*)$"

search = 4000000
search_space = Polygon([(0, 0), (0, search), (search, search), (search, 0)])
sensors = []

for line in lines:
    sx, sy, bx, by = [int(c) for c in re.split(formatting, line)[1:-1]]
    d = abs(sx - bx) + abs(sy - by)

    sensor = Polygon([(sx, sy - d), (sx + d, sy), (sx, sy + d), (sx - d, sy)])
    sensors.append(sensor)

possible_area = np.array(search_space.difference(unary_union(sensors)).exterior.coords)

hidden_beacon = np.mean(possible_area, axis=0)

print(search * int(hidden_beacon[0]) + int(hidden_beacon[1]))

print(time.time() - start_time)
