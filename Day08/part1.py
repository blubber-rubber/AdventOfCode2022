import time
import numpy as np

start_time = time.time()

with open('input.txt') as f:
    lines = [[int(i) for i in line.rstrip('\n')] for line in f.readlines()]

grid = np.zeros((len(lines), len(lines[0])))


def get_vis_index(row):
    highest = -1
    visual = []
    for index, tree in enumerate(row):
        if tree > highest:
            visual.append(index)
            highest = tree
    return visual


def transpose(grid):
    return [[grid[i][j] for i in range(len(grid))] for j in range(len(grid[0]))]


for i, row in enumerate(lines):
    visual1 = get_vis_index(row)
    visual2 = get_vis_index(row[::-1])

    for vis in visual1:
        grid[i, vis] = 1
    for vis in visual2:
        grid[i, len(row) - 1 - vis] = 1

grid = grid.T

for i, row in enumerate(transpose(lines)):
    visual1 = get_vis_index(row)
    visual2 = get_vis_index(row[::-1])

    for vis in visual1:
        grid[i, vis] = 1
    for vis in visual2:
        grid[i, len(row) - 1 - vis] = 1

print(int(np.sum(grid)))
print(time.time() - start_time)
