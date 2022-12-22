import time

start_time = time.time()


def preprocess(line):
    if '[' not in line:
        return int(line)

    line = line[1:-1]
    parts = []
    index = 0
    start = 0
    while index < len(line):
        if line[index] == ',':
            parts.append(preprocess(line[start:index]))
            start = index + 1
        elif line[index] == "[":
            start = index
            n_brackets = 1
            index += 1
            while n_brackets > 0:
                if line[index] == "[":
                    n_brackets += 1
                elif line[index] == "]":
                    n_brackets -= 1
                index += 1
            parts.append(preprocess(line[start:index]))
            start = index + 1
        index += 1
    if index > start:
        parts.append(preprocess(line[start:index]))
    return parts


with open('input.txt') as f:
    packet_pairs = []
    lines = [line.rstrip('\n') for line in f.readlines()]
    index = 0
    while index < len(lines):
        line1 = preprocess(lines[index])
        line2 = preprocess(lines[index + 1])
        index += 3
        packet_pairs.append((line1, line2))


def compare(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return (p1 < p2) - (p1 > p2)
    elif isinstance(p1, list) and isinstance(p2, list):
        i = 0
        while i < len(p1) and i < len(p2):
            test = compare(p1[i], p2[i])
            if test != 0:
                return test
            i += 1
        return (len(p1) < len(p2)) - (len(p1) > len(p2))
    elif isinstance(p1, int):
        return compare([p1], p2)
    else:
        return compare(p1, [p2])


score = 0
for index, pair in enumerate(packet_pairs):
    score += (index + 1) * (compare(*pair) >= 0)
print(score)
print(time.time() - start_time)
