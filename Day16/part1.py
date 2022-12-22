import time
import re
from collections import defaultdict

start_time = time.time()
formatting = "^Valve ([A-Z]*) has flow rate=([0-9]*); tunnel[s]* lead[s]* to valve[s]* ([A-Z, ]*)$"


class Valve:

    def __init__(self):
        self.name = None
        self.tunnels = None
        self.flow_rate = None

    def initialize(self, name, tunnels, flow_rate):
        self.name = name
        self.tunnels = tunnels
        self.flow_rate = flow_rate


valves = defaultdict(Valve)

with open('input.txt') as f:
    lines = []
    for line in f.readlines():
        name, flow_rate, tunnels = re.split(formatting, line.rstrip("\n"))[1:-1]
        valve = valves[name]
        valve.initialize(name, tunnels.split(', '), int(flow_rate))

relevant_valves = {key: item for key, item in valves.items() if item.flow_rate > 0}
not_opened = set(relevant_valves.keys())
relevant_valves["AA"] = valves["AA"]

distances = {}
for name, valve in relevant_valves.items():
    distance2valve = dict()
    visited = {name}
    current_pos = [name]
    d = 1
    while len(visited) != len(valves):
        new_pos = []
        for pos in current_pos:
            for neighbour in [n for n in valves[pos].tunnels if n not in visited]:
                if neighbour in relevant_valves:
                    distance2valve[neighbour] = d
                new_pos.append(neighbour)
                visited.add(neighbour)
        current_pos = new_pos
        d += 1
    distances[name] = distance2valve


path = ["AA"]


def remaining_score(time, pos, dest):
    return max(0, (30 - time - 1 - distances[pos][dest]) * relevant_valves[dest].flow_rate)


def branch_and_bound(path, time, score, not_opened, max_score):
    if time >= 30:
        max_score = max(score, max_score)
        return max_score
    pos = path[-1]
    for dest in sorted(not_opened, key=lambda x: remaining_score(time, pos, x), reverse=True):
        path.append(dest)
        not_opened.remove(dest)
        max_score = branch_and_bound(path, time + distances[pos][dest] + 1, score + remaining_score(time, pos, dest),
                                     not_opened, max_score)
        not_opened.add(dest)
        path.pop(-1)

    return max_score


print(branch_and_bound(["AA"], 0, 0, not_opened, 0))

print(time.time() - start_time)
