import time

start_time = time.time()

with open("input.txt", 'r') as f:
    lines = f.readlines()

result_scores = {("A", "X"): 3, ("B", "X"): 0, ("C", "X"): 6,
                 ("A", "Y"): 6, ("B", "Y"): 3, ("C", "Y"): 0,
                 ("A", "Z"): 0, ("B", "Z"): 6, ("C", "Z"): 3, }

choice_score = {"X": 1, "Y": 2, "Z": 3, }

score = 0
for line in lines:
    opp, resp = line.rstrip("\n").split(" ")
    score += choice_score[resp] + result_scores[(opp, resp)]

print(score)

print(time.time() - start_time)
