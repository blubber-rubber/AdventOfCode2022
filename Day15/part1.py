import time
import re

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

formatting = "^Sensor at x=([\-0-9]*), y=([\-0-9]*): closest beacon is at x=([\-0-9]*), y=([\-0-9]*)$"

relevant_level = 2000000
blocked_on_level = set()
beacons = set()

for line in lines:
    sx, sy, bx, by = [int(c) for c in re.split(formatting, line)[1:-1]]
    distance_covered = abs(sx - bx) + abs(sy - by)
    distanc_to_relevant_level = abs(sy - relevant_level)
    if by == relevant_level:
        beacons.add(bx)

    if distance_covered >= distanc_to_relevant_level:
        d = distance_covered - distanc_to_relevant_level
        blocked_on_level.update(range(sx - d, sx + d + 1))

print(len(blocked_on_level.difference(beacons)))
print(time.time() - start_time)
