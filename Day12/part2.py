import time
import numpy as np

start_time = time.time()

with open('input.txt') as f:
    grid = np.array([[ord(c) - 97 if ord(c) >= 97 else c for c in line.rstrip('\n')] for line in f.readlines()])

current_pos = tuple(int(x) for x in list(zip(*np.where(grid == "S")))[0])
end_pos = tuple(int(x) for x in list(zip(*np.where(grid == "E")))[0])

grid[current_pos] = 0
grid[end_pos] = 25

grid = grid.astype(int)


def get_neighbours(pos, visited):
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbours = [(pos[0] + d[0], pos[1] + d[1]) for d in DIRECTIONS if
                  0 <= pos[0] + d[0] < len(grid) and 0 <= pos[1] + d[1] < len(grid[0]) and (
                      pos[0] + d[0], pos[1] + d[1]) not in visited and grid[pos] - 1 <= grid[(
                      pos[0] + d[0], pos[1] + d[1])]]
    return neighbours


##############################
visited = {end_pos}
current_depth = {end_pos}
distance = 0

found = False

while not found:
    new_depth = set()
    distance += 1
    for d in current_depth:
        neighbours = get_neighbours(d, visited)
        new_depth.update(neighbours)
        visited.update(neighbours)
    current_depth = new_depth

    found = any(grid[p] == 0 for p in visited)

print(distance)

print(time.time() - start_time)
