import time

start_time = time.time()

with open("input.txt", "r") as f:
    lines = "".join(f.readlines())

calories = []

for elf in lines.split("\n\n"):
    calories.append(sum([int(x) for x in elf.split("\n")]))

print(max(calories))
print(time.time() - start_time)
