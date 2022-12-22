import time

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

register = 1
cycle = 1


def during_cycle(cycle_number, register, result, crt):
    pixel_number = (cycle_number - 1) % 40
    if register - 1 <= pixel_number <= register + 1:
        crt.append("█")
    else:
        crt.append(' ')
    if pixel_number == 39:
        result.append("".join(crt))
        crt = []
    return crt


result = []
crt = []
for line in lines:
    if line.startswith('noop'):
        crt = during_cycle(cycle, register, result, crt)
        cycle += 1
    else:
        n = int(line.split(' ')[1])
        crt = during_cycle(cycle, register, result, crt)
        cycle += 1
        crt = during_cycle(cycle, register, result, crt)
        cycle += 1
        register += n


for row in result:
    print(row)

print(time.time() - start_time)
