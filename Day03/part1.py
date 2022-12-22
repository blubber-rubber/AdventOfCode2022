import time

start_time = time.time()

with open("input.txt", "r") as f:
    backpacks = [line.rstrip('\n') for line in f.readlines()]

score = 0
for backpack in backpacks:
    comp1 = set(char for char in backpack[:len(backpack) // 2])
    comp2 = set(char for char in backpack[len(backpack) // 2:])
    common_item = list(comp1.intersection(comp2))[0]
    if common_item.islower():
        score += ord(common_item) - 96
    else:
        score += ord(common_item) - 38

print(score)

print(time.time() - start_time)
