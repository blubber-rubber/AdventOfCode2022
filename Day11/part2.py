import time
import numpy as np

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

MONKEYS = dict()
MOD = 1


class Monkey:
    def __init__(self, number, operation, test, items, friends, constant):
        self.number = number
        self.operation = operation
        self.test = test
        self.items = items
        self.friends = friends
        self.inspections = 0
        self.constant = constant

    def investigate(self):
        self.items = [self.operation(t, self.constant) for t in self.items]
        self.inspections += len(self.items)

    def bored(self):
        self.items = [t % MOD for t in self.items]

    def throw(self):
        for t in self.items:
            MONKEYS[self.friends[t % self.test == 0]].items.append(t)
        self.items = []

    def update(self):
        self.investigate()
        self.bored()
        self.throw()


index = 0
while index < len(lines):
    number = int(lines[index].rstrip(':').split(' ')[1])
    index += 1
    items = [int(x) for x in lines[index][len('  Starting items: '):].split(',')]
    index += 1
    operation_line = lines[index][len('  Operation: new = old '):]
    symbol, n = operation_line.split(' ')

    if n == "old":
        constant = 1
        operation = lambda x, y: x ** 2
    elif symbol == "*":
        constant = int(n)
        operation = lambda x, y: x * y
    else:
        constant = int(n)
        operation = lambda x, y: x + y

    index += 1
    test = int(lines[index][len('  Test: divisible by '):])
    index += 1
    friends = {1: int(lines[index][len('    If true: throw to monkey '):]),
               0: int(lines[index + 1][len('    If false: throw to monkey '):])}
    index += 3

    MONKEYS[number] = Monkey(number, operation, test, items, friends, constant)

MOD = int(np.prod([m.test for m in MONKEYS.values()]))

ITERATIONS = 10000
for i in range(ITERATIONS):
    for monkey in sorted(MONKEYS.keys()):
        MONKEYS[monkey].update()

monkey_business = list(sorted(MONKEYS.values(), key=lambda m: -m.inspections))[:2]
print(monkey_business[0].inspections * monkey_business[1].inspections)
print(time.time() - start_time)
