import time

start_time = time.time()

with open('input.txt') as f:
    container_lines = []
    line = f.readline().rstrip('\n')
    while line:
        container_lines.append(line)
        line = f.readline().rstrip('\n')

    instructions = [
        tuple(int(i) for i in line.rstrip('\n').lstrip('move').replace(' from ', ',').replace(' to ', ',').split(','))
        for line in f.readlines()]

n_containers = max(int(i) for i in container_lines[-1].strip(' ').split('   '))
containers = [[] for i in range(n_containers)]
for line in container_lines[-2::-1]:
    for i, c in enumerate(line[1:n_containers * 4 + 1: 4]):
        if c != ' ':
            containers[i].append(c)

for inst in instructions:
    temp = []
    for _ in range(inst[0]):
        temp.append(containers[inst[1] - 1].pop(-1))
    containers[inst[2] - 1].extend(temp[::-1])
print(''.join(c[-1] for c in containers))

print(time.time() - start_time)
