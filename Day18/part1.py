import time
import numpy as np

start_time = time.time()

with open('input.txt') as f:
    lines = [np.array([int(i) for i in line.rstrip('\n').split(',')]) for line in f.readlines()]

directions = [np.array([0 + d * (pos == 0), 0 + d * (pos == 1), 0 + d * (pos == 2)]) for d in [-1, 1] for pos in
              range(3)]

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
