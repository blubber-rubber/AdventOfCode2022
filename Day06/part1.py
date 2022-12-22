import time

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

line = "".join(lines)
i = 0

while len(set(line[i:i + 4])) < 4:
    i += 1

print(i+4)
print(time.time() - start_time)
