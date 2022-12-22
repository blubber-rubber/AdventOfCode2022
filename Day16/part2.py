import time
import re
from collections import defaultdict
from itertools import combinations

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

path1 = ["AA"]
path2 = ["AA"]


def remaining_score(t, valve):
    return max(0, (26 - t) * relevant_valves[valve].flow_rate)


possible_paths = []


def dfs(path, not_opened):
    added = False
    pos, t = path[-1]
    if t >= 26 or not not_opened:
        possible_paths.append(path.copy())
    else:

        for n in sorted(not_opened, key=lambda x: distances[pos][x]):
            new_time = t + distances[pos][n] + 1
            if new_time >= 26:
                if not added:
                    possible_paths.append(path.copy())
                    added = True
            else:
                not_opened.remove(n)
                path.append((n, new_time))
                dfs(path, not_opened)
                path.pop(-1)
                not_opened.add(n)
                added = True


dfs([('AA', 0)], not_opened)

max_pressure = 0


def get_path_pressure(path):
    visited = set()
    pressure = 0
    for v, t in path:
        if v not in visited:
            pressure += remaining_score(t, v)
            visited.add(v)
    return pressure


possible_paths.sort(reverse=True, key=lambda x: get_path_pressure(x))
index = 0
for path1, path2 in combinations(possible_paths, 2):
    path = path1 + path2
    path.sort(key=lambda x: x[1])
    pressure = get_path_pressure(path)
    if pressure > max_pressure:
        max_pressure = pressure
    if index>100000:
        break
    index+=1

print(max_pressure)

print(time.time() - start_time)
