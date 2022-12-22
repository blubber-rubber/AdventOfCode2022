import time

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]


class Rope_piece:

    def __init__(self, name, previous):
        self.name = name
        self.previous = previous
        self.pos = (0, 0)
        self.coords = [self.pos]

    def touching_previous(self):
        return abs(self.pos[0] - self.previous.pos[0]) <= 1 and abs(self.pos[1] - self.previous.pos[1]) <= 1

    def follow(self):
        if not self.touching_previous():
            new_pos = self.previous.coords[-2]
            self.coords.append(new_pos)
            self.pos = new_pos

    def move(self, direction):
        new_pos = (direction[0] + self.pos[0], direction[1] + self.pos[1])
        self.coords.append(new_pos)
        self.pos = new_pos


head = Rope_piece("HEAD", None)
tail = Rope_piece("Tail", head)

directions = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}

for line in lines:
    direction, n = directions[line[0]], int(line[2:])
    for _ in range(n):
        head.move(direction)
        tail.follow()

print(len(set(tail.coords)))
print(time.time() - start_time)

