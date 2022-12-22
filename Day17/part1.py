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

while rock_index < 2022:
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
            max_height = max(max_height, pos[1] + upper[r_index])
    # print("\n".join(["".join(["#" if (x, y) in filled else "." for x in range(7)]) for y in range(max_height, 0, -1)]))
    # print('-----------------------')
    rock_index += 1

print(max_height)
print(time.time() - start_time)
