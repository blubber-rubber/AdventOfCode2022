with open('input.txt', 'r') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

score = 0
for line in lines:
    elf1, elf2 = [tuple(int(i) for i in job.split('-')) for job in line.split(',')]
    if elf1[1] - elf1[0] < elf2[1] - elf2[0]:
        elf1, elf2 = elf2, elf1

    if elf1[0] <= elf2[0] <= elf1[1] or elf2[0] <= elf1[0] <= elf2[1]:
        score += 1

print(score)
