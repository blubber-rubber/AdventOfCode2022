import time
from collections import defaultdict

start_time = time.time()

DIRECTIONS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

cardinal_directions = [(0, 1, 2), (4, 5, 6), (6, 7, 0), (2, 3, 4)]

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

elves = list((x, y) for y, line in enumerate(lines) for x in range(len(line)) if line[x] == '#')
elves_pos = set(elves)
moving = True
N_ROUNDS = 10

round_index = 0

direction_index = 0
counter = defaultdict(int)

while moving and round_index < N_ROUNDS:
    considered_positions = []
    counter = defaultdict(int)
    for elf in elves:
        direction_checks = [(elf[0] + d[0], elf[1] + d[1]) in elves_pos for d in DIRECTIONS]
        if not any(direction_checks):
            considered_positions.append(elf)
            counter[elf] += 1
        else:
            thinking = True
            index = 0
            while index < 4 and thinking:
                if not any(
                        direction_checks[k] for k in
                        cardinal_directions[(direction_index + index) % len(cardinal_directions)]):
                    dir = DIRECTIONS[cardinal_directions[(direction_index + index) % len(cardinal_directions)][1]]
                    new_pos = (elf[0] + dir[0], elf[1] + dir[1])
                    considered_positions.append(new_pos)
                    counter[new_pos] += 1
                    thinking = False
                index += 1
            if thinking:
                considered_positions.append(elf)
                counter[elf] += 1

    new_elves = []
    for i, elf in enumerate(elves):

        if counter[considered_positions[i]] <= 1:
            new_elves.append(considered_positions[i])
        else:
            new_elves.append(elf)

    elves = new_elves
    new_elves_pos = set(elves)

    if not new_elves_pos.difference(elves_pos):
        moving = False

    elves_pos = new_elves_pos

    round_index += 1
    direction_index = (direction_index + 1) % len(cardinal_directions)

minx = min(elf[0] for elf in elves)
maxx = max(elf[0] for elf in elves)
miny = min(elf[1] for elf in elves)
maxy = max(elf[1] for elf in elves)

print((maxx - minx + 1) * (maxy - miny + 1) - len(elves))
print(time.time() - start_time)
