import time

start_time = time.time()

with open("input.txt", "r") as f:
    backpacks = [line.rstrip('\n') for line in f.readlines()]

score = 0
for i in range(0, len(backpacks), 3):
    b1 = set(backpacks[i])
    b2 = set(backpacks[i + 1])
    b3 = set(backpacks[i + 2])
    common_item = list(b1.intersection(b2).intersection(b3))[0]
    if common_item.islower():
        score += ord(common_item) - 96
    else:
        score += ord(common_item) - 38

print(score)

print(time.time() - start_time)
