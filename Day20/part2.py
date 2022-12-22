import time

start_time = time.time()

with open('input.txt') as f:
    lines = [int(line.rstrip('\n')) for line in f.readlines()]

decryption_key = 811589153


class linked_list:

    def __init__(self, val, prev):
        self.val = val * decryption_key
        self.prev = prev
        self.next = None

    def set_next(self, next):
        self.next = next

    def set_prev(self, prev):
        self.prev = prev


nodes = []

for line in lines:
    prev = None if not nodes else nodes[-1]
    node = linked_list(line, prev)
    if prev:
        prev.set_next(node)
    nodes.append(node)
nodes[-1].set_next(nodes[0])
nodes[0].set_prev(nodes[-1])

for i in range(10):
    for node in nodes:
        prev = node.prev
        next = node.next
        next.set_prev(prev)
        prev.set_next(next)
        val = node.val % (len(nodes) - 1)
        if (len(nodes) - 1) - val < val:
            val = val - len(nodes) + 1
        if val >= 0:
            for _ in range(val):
                prev = prev.next
                next = next.next
        else:
            for _ in range(-val):
                prev = prev.prev
                next = next.prev

        prev.set_next(node)
        next.set_prev(node)
        node.set_next(next)
        node.set_prev(prev)

zero_node = [node for node in nodes if node.val == 0][0]

result = []

for i in range(3):
    for j in range(1000):
        zero_node = zero_node.next
    result.append(zero_node.val)

print(sum(result))

print(time.time() - start_time)
