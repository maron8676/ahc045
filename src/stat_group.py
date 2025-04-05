from sys import stdin
from collections import defaultdict

readline = stdin.readline


def li():
    return list(map(int, readline().split()))


group_num = [0] * 801
for i in range(100):
    with open(f"in/{i:04}.txt", mode="r", encoding="utf8") as f:
        f.readline()
        G = f.readline().split()
        for g in G:
            group_num[int(g)] += 1

cum = 0
cum2 = 0
print(sum(group_num))
for item in enumerate(group_num):
    cum += item[1]
    cum2 += item[0] * item[1]
    print(item, cum, cum / sum(group_num), cum2 / 80000)
