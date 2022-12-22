import time
import re
import math
from tqdm import tqdm

start_time = time.time()

TIME_LIMIT = 24

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

formatting = "^Blueprint ([0-9]*): Each ore robot costs ([0-9]*) ore. Each clay robot costs ([0-9]*) ore. Each obsidian robot costs ([0-9]*) ore and ([0-9]*) clay. Each geode robot costs ([0-9]*) ore and ([0-9]*) obsidian.$"

readable = ["bp_id", "ore_req1", "ore_req2", "ore_req3", "clay_req3", "ore_req4", "obs_req4"]

tiers = ["geo", "obs", "clay", "ore"]


def find_possible(robots, inventory, reqs, rem):
    new_ore_r = math.ceil((reqs["ore_req1"] - inventory["ore"]) / robots["ore"])
    new_clay_r = math.ceil((reqs["ore_req2"] - inventory["ore"]) / robots["ore"])
    new_obs_r = 2 * TIME_LIMIT if robots["clay"] == 0 else max(
        math.ceil((reqs["clay_req3"] - inventory["clay"]) / robots["clay"]),
        math.ceil((reqs["ore_req3"] - inventory["ore"]) / robots["ore"]))
    new_geo_r = 2 * TIME_LIMIT if robots["obs"] == 0 else max(
        math.ceil((reqs["obs_req4"] - inventory["obs"]) / robots["obs"]),
        math.ceil((reqs["ore_req4"] - inventory["ore"]) / robots["ore"]))

    if reqs["clay_req3"] * rem <= inventory["clay"] + rem * robots["clay"]:
        new_clay_r = 2 * TIME_LIMIT

    if reqs["obs_req4"] * rem <= inventory["obs"] + robots["obs"] * rem:
        new_obs_r = 2 * TIME_LIMIT

    if all(reqs[f'ore_req{i}'] * rem <= inventory['ore'] + rem * robots['ore'] for i in range(1, 5)):
        new_ore_r = 2 * TIME_LIMIT

    return {"ore": max(1, 1 + new_ore_r), "clay": max(1, 1 + new_clay_r), "obs": max(1, 1 + new_obs_r),
            "geo": max(1, 1 + new_geo_r)}


rob2reqs = {"ore": ["ore_req1"], "clay": ["ore_req2"], "obs": ["ore_req3", "clay_req3"],
            "geo": ["ore_req4", "obs_req4"]}


def dfs(time, robots, inventory, reqs, results):
    time_remaining = TIME_LIMIT - time
    time_skips = find_possible(robots, inventory, reqs, time_remaining)
    relevant_skips = [(r, t) for r, t in time_skips.items() if
                      time + t <= TIME_LIMIT and inventory['geo'] + time_remaining * robots["geo"] + (
                              time_remaining - 1) * time_remaining / 2 > results[reqs["bp_id"] - 1]]
    if not relevant_skips:
        results[reqs["bp_id"] - 1] = max(results[reqs["bp_id"] - 1], inventory["geo"] + time_remaining * robots["geo"])
        return
    for rob, time_skip in sorted(relevant_skips, key=lambda x: tiers.index(x[0])):
        new_inventory = {}
        for key in inventory.keys():
            new_inventory[key] = inventory[key] + time_skip * robots[key]

        robots[rob] += 1
        for req in rob2reqs[rob]:
            p1, _ = req.split('_')
            new_inventory[p1] -= reqs[req]

        dfs(time + time_skip, robots, new_inventory, reqs, results)

        robots[rob] -= 1


results = []
for line in tqdm(lines):
    reqs = {readable[i]: int(r) for i, r in enumerate(re.split(formatting, line)[1:-1])}
    robots = {"ore": 1, "clay": 0, "obs": 0, "geo": 0}
    inventory = {"ore": 0, "clay": 0, "obs": 0, "geo": 0}
    results.append(0)
    dfs(0, robots, inventory, reqs, results)

print(sum((i + 1) * r for i, r in enumerate(results)))
print(time.time() - start_time)
