import time

start_time = time.time()

with open("input.txt", 'r') as f:
    lines = f.readlines()

tactics = {("A", "X"): "C", ("B", "X"): "A", ("C", "X"): "B",
                 ("A", "Y"): "A", ("B", "Y"): "B", ("C", "Y"): "C",
                 ("A", "Z"): "B", ("B", "Z"): "C", ("C", "Z"): "A", }

result_scores = {"X": 0, "Y": 3, "Z": 6}
choice_score = {"A": 1, "B": 2, "C": 3}

score = 0
for line in lines:
    opp, result = line.rstrip("\n").split(" ")
    score += choice_score[tactics[(opp, result)]] + result_scores[result]

print(score)



print(time.time() - start_time)