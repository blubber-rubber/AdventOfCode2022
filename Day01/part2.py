import time

start_time = time.time()

with open("input.txt", "r") as f:
    lines = "".join(f.readlines())

calories = []

for elf in lines.split("\n\n"):
    calories.append(sum([int(x) for x in elf.split("\n")]))

calories.sort(reverse=True)

print(sum(calories[:3]))
print(time.time() - start_time)

