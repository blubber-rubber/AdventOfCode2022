import time

start_time = time.time()

with open('input.txt') as f:
    wall_points = [[tuple(int(x) for x in p.split(',')) for p in line.rstrip('\n').split(' -> ')] for line in
                   f.readlines()]

WALLS = set()
START_POSITION = (500, 0)


def add_wall(p1, p2):
    p1, p2 = sorted([p1, p2])
    if p1[0] == p2[0]:
        for y in range(p1[1], p2[1] + 1):
            WALLS.add((p1[0], y))
    else:
        for x in range(p1[0], p2[0] + 1):
            WALLS.add((x, p1[1]))


for points in wall_points:
    for p1, p2 in zip(points, points[1:]):
        add_wall(p1, p2)

floor_height = max(w[1] for w in WALLS) + 2
for x in range(500 - 2 * floor_height, 500 + 2 * floor_height):
    WALLS.add((x, floor_height))


def fall_down(path, grains):
    pos = path[-1]
    downs = [(pos[0], pos[1] + 1), (pos[0] - 1, pos[1] + 1), (pos[0] + 1, pos[1] + 1)]
    for d in downs:
        if d not in WALLS and d not in grains:
            path.append(d)
            fall_down(path, grains)
            path.pop(-1)
    grains.add(pos)


grains = set()
fall_down([START_POSITION], grains)

print(len(grains))

print(time.time() - start_time)
