import time

start_time = time.time()

rocks = [[(0, 0), (1, 0), (2, 0), (3, 0)],
         [(1, 0), (1, 1), (0, 1), (1, 2), (2, 1)],
         [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
         [(0, 0), (0, 1), (0, 2), (0, 3)],
         [(0, 0), (1, 0), (1, 1), (0, 1)],
         ]

most_rights = [max(c[0] for c in lijst) for lijst in rocks]
upper = [max(c[1] for c in lijst) for lijst in rocks]
filled = set((i, 0) for i in range(7))

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

instructions = lines[0]

rock_index = 0
instr_index = 0
max_height = 0
temp = 0
reps = []
rep_found = False

from collections import Counter


def find_rep(filled):
    full_levels = [i for i in range(1, max_height + 1) if all((x, i) in filled for x in range(7))]
    reps = [j - i for i, j in zip(full_levels, full_levels[1:])]
    if not reps:
        return None
    rep_start = Counter(reps).most_common(1)[0]
    if rep_start[1] < 2:
        return None

    indices = [i for i in range(len(reps)) if reps[i] == rep_start[0]][:2]

    if len(reps) < 2 * indices[1] - indices[0]:
        return None
    i1, i2 = indices
    check = True
    for d in range(i2 - i1):
        check = check and reps[i1 + d] == reps[i2 + d]
    if check:
        return full_levels[i1], full_levels[i2]

    return None


rep = None

pos2rock = dict()

while rep is None:
    r_index = rock_index % len(rocks)
    rock = rocks[r_index]
    pos = [2, max_height + 4]
    moving = True
    while moving:
        instr = instructions[instr_index % len(instructions)]
        if instr == ">":
            if all((pos[0] + c[0] + 1, pos[1] + c[1]) not in filled for c in rock) and pos[0] + most_rights[
                r_index] + 1 < 7:
                pos[0] += 1
        else:
            if all((pos[0] + c[0] - 1, pos[1] + c[1]) not in filled for c in rock) and pos[0] - 1 >= 0:
                pos[0] -= 1
        instr_index += 1
        if all((pos[0] + c[0], pos[1] + c[1] - 1) not in filled for c in rock):
            pos[1] -= 1
        else:
            moving = False
            filled.update((pos[0] + c[0], pos[1] + c[1]) for c in rock)
            for c in rock:
                pos2rock[(pos[0] + c[0], pos[1] + c[1])] = rock_index
            max_height = max(max_height, pos[1] + upper[r_index])
    # print("\n".join(["".join(["#" if (x, y) in filled else "." for x in range(7)]) for y in range(max_height, 0, -1)]))
    # print('-----------------------')
    rock_index += 1

    rep = find_rep(filled)

relevant_rocks = set([pos2rock[(i, rep[0])] for i in range(7)])
h1 = max([(x, y) for x, y in filled if y > 0 and pos2rock[(x, y)] in relevant_rocks], key=lambda p: p[1])
ref_rock1 = pos2rock[h1]

relevant_rocks = set([pos2rock[(i, rep[1])] for i in range(7)])
h2 = max([(x, y) for x, y in filled if y > 0 and pos2rock[(x, y)] in relevant_rocks], key=lambda p: p[1])
ref_rock2 = pos2rock[h2]

height_delta = h2[1] - h1[1]

rock_delta = ref_rock2 - ref_rock1

N = 1000000000000

remaining_height = max([(x, y) for x, y in filled if y > 0 and pos2rock[(x, y)] == (N - ref_rock1 - 1) % rock_delta + ref_rock1],
    key=lambda p: p[1])[1]
height = ((N - ref_rock1 - 1) // rock_delta) * height_delta + remaining_height

print(height)
print(time.time() - start_time)
