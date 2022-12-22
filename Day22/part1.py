import time
import re
import numpy as np

symbols = [">", "v", "<", "^"]

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

start_time = time.time()

with open('input.txt') as f:
    lines = [[x for x in line.rstrip('\n')] for line in f.readlines()]

grid = lines[:-2]
instructions = "".join(lines[-1])


def take_steps(pos, l, d_index):
    step_index = 0
    moved = True
    while step_index < l and moved:
        new_x = pos[0] + DIRECTIONS[d_index][0]
        new_y = pos[1] + DIRECTIONS[d_index][1]

        in_grid = (0 <= new_y < len(grid)) and (0 <= new_x < len(grid[new_y])) and (grid[new_y][new_x] != " ")

        if not in_grid:
            if d_index == 1:
                new_y = 0
                while new_x >= len(grid[new_y]) or grid[new_y][new_x] == ' ':
                    new_y += 1

            elif d_index == 3:
                new_y = len(grid) - 1
                while new_x >= len(grid[new_y]) or grid[new_y][new_x] == ' ':
                    new_y -= 1

            elif d_index == 0:
                new_x = 0
                while grid[new_y][new_x] == ' ':
                    new_x += 1

            elif d_index == 2:
                new_x = len(grid[new_y]) - 1
                while grid[new_y][new_x] == ' ':
                    new_x -= 1

        if grid[new_y][new_x] == '#':
            moved = False
        else:
            grid[pos[1]][pos[0]] = symbols[d_index]
            pos = [new_x, new_y]
        step_index += 1
    return pos


pos = [grid[0].index('.'), 0]

d_index = 0
start_index = 0
end_index = 0
while end_index < len(instructions):
    while end_index < len(instructions) and not instructions[end_index] in 'LR':
        end_index += 1

    instr_l = int(instructions[start_index:end_index])
    instr_r = None if end_index >= len(instructions) else instructions[end_index]

    pos = take_steps(pos, instr_l, d_index)

    if instr_r:
        d_index = (d_index + 2 * (instr_r == "R") - 1) % len(DIRECTIONS)

    end_index += 1
    start_index = end_index

print((pos[1] + 1) * 1000 + (pos[0] + 1) * 4 + d_index)
print(time.time() - start_time)

grid[pos[1]][pos[0]] = symbols[d_index]
#print('\n'.join(["".join([p for p in line]) for line in grid]))
