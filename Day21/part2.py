import sympy as sp
import time
from collections import defaultdict


def plus(children):
    return f'({children[0].val}) + ({children[1].val})'


def minus(children):
    return f'({children[0].val}) - ({children[1].val})'


def multiply(children):
    return f'({children[0].val}) * ({children[1].val})'


def divide(children):
    return f'({children[0].val}) / ({children[1].val})'


class Monkey:

    def __init__(self):
        self.name = None
        self.operation = None
        self.children = []
        self.val = None

    def set_name(self, name):
        self.name = name

    def set_operation(self, operation):
        self.operation = operation

    def add_child(self, child):
        self.children.append(child)

    def perform(self):
        if self.operation is not None:
            self.val = self.operation(self.children)


OPERATORS = {" * ": multiply, " + ": plus, " - ": minus, " / ": divide}

start_time = time.time()

monkeys = defaultdict(Monkey)

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

for line in lines:
    current_monkey_name, op = line.split(': ')
    current_monkey = monkeys[current_monkey_name]
    current_monkey.set_name(current_monkey_name)

    no_operation = True
    for operator, operation in OPERATORS.items():
        if operator in op:
            m1_name, m2_name = op.split(operator)
            m1, m2 = monkeys[m1_name], monkeys[m2_name]
            current_monkey.add_child(m1)
            current_monkey.add_child(m2)
            current_monkey.set_operation(operation)
            no_operation = False
            break
    if no_operation:
        current_monkey.val = op

monkeys['humn'].val = "x"


def calculate(current_monkey):
    if current_monkey.val is None:
        for child in current_monkey.children:
            calculate(child)
        current_monkey.perform()


left, right = monkeys["root"].children
calculate(left)
calculate(right)

eq = sp.Eq(sp.sympify(left.val), sp.sympify(right.val))
result = sp.solve(eq, sp.symbols("x"))
print(int(result[0]))

print(time.time() - start_time)
