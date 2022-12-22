import time

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

register = 1
cycle = 1


def end_cycle(cycle_number, register, result):
    if cycle_number % 40 == 20:
        result.append(cycle_number * register)


result = []
for line in lines:
    if line.startswith('noop'):
        end_cycle(cycle, register, result)
        cycle += 1
    else:
        n = int(line.split(' ')[1])
        end_cycle(cycle, register, result)
        cycle += 1
        end_cycle(cycle, register, result)
        cycle += 1
        register += n


print(sum(result))
print(time.time() - start_time)
