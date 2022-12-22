import time
import numpy as np
from collections import defaultdict

start_time = time.time()

with open('input.txt') as f:
    lines = [[int(i) for i in line.rstrip('\n')] for line in f.readlines()]

grid = np.zeros((len(lines), len(lines[0])))


def scenic_score(row):
    last_seen = defaultdict(int)
    trees = set()
    scores = []
    for index, tree in enumerate(row):
        trees.add(tree)
        scores.append(index - max([last_seen[t] for t in trees if t >= tree]))
        last_seen[tree] = index
    return scores


def transpose(grid):
    return [[grid[i][j] for i in range(len(grid))] for j in range(len(grid[0]))]


dir1 = []
dir2 = []
dir3 = []
dir4 = []

for i, row in enumerate(lines):
    dir1.append(scenic_score(row))
    dir2.append(scenic_score(row[::-1])[::-1])

grid = grid.T

for i, row in enumerate(transpose(lines)):
    dir3.append(scenic_score(row))
    dir4.append(scenic_score(row[::-1])[::-1])

dir1 = np.array(dir1)
dir2 = np.array(dir2)
dir3 = np.array(dir3).T
dir4 = np.array(dir4).T

print(int(np.max(dir1 * dir2 * dir3 * dir4)))
print(time.time() - start_time)
