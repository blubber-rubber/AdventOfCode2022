import time

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

line = "".join(lines)
i = 0

while len(set(line[i:i + 14])) < 14:
    i += 1

print(i+14)
print(time.time() - start_time)
