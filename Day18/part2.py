import time
import numpy as np

start_time = time.time()

with open('input.txt') as f:
    lines = [np.array([int(i) for i in line.rstrip('\n').split(',')]) for line in f.readlines()]

directions = [np.array([0 + d * (pos == 0), 0 + d * (pos == 1), 0 + d * (pos == 2)]) for d in [-1, 1] for pos in
              range(3)]

drop = set(tuple(line) for line in lines)

minx, maxx = min(c[0] for c in drop) - 1, max(c[0] for c in drop) + 1
miny, maxy = min(c[1] for c in drop) - 1, max(c[1] for c in drop) + 1
minz, maxz = min(c[2] for c in drop) - 1, max(c[2] for c in drop) + 1
mins = np.array([minx, miny, minz])
maxs = np.array([maxx, maxy, maxz])

current_pos = [(minx, miny, minz)]
outside = set()

while current_pos:
    pos = current_pos.pop(0)
    for d in directions:
        new_pos = tuple(np.array(pos) + d)
        if new_pos not in drop and new_pos not in outside and all(mins <= new_pos) and all(new_pos <= maxs):
            outside.add(new_pos)
            current_pos.append(new_pos)

inside = set(
    (x, y, z) for x in range(minx, maxx + 1) for y in range(miny, maxy + 1) for z in range(minz, maxz + 1)).difference(
    outside)

lines = []
for i in inside:
    lines.append(np.array(i))

cubes = {}

for line in lines:
    pos = tuple(line)
    cubes[pos] = []
    for d in directions:
        neighbour = tuple(line + d)
        if neighbour in cubes:
            cubes[neighbour].append(pos)
            cubes[pos].append(neighbour)

print(sum(6 - len(neighs) for neighs in cubes.values()))

print(time.time() - start_time)
