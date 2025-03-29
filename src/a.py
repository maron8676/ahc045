import sys
from collections import defaultdict, deque
from sys import stdin

readline = stdin.readline


class City:
    def __init__(self, index, lx, rx, ly, ry):
        self.index = index
        self.lx = lx
        self.rx = rx
        self.ly = ly
        self.ry = ry

    def __str__(self):
        return f"City[{self.index}, {self.mean()}]"

    def mean(self):
        return [(self.lx + self.rx) // 2, (self.ly + self.ry) // 2]


def li():
    return list(map(int, readline().split()))


def query(c: list[City]):
    print("?", len(c), *list(map(lambda x: x.index, c)), flush=True)
    return [tuple(map(int, input().split())) for _ in range(len(c) - 1)]


def answer(groups, edges):
    print("!")
    for i in range(len(groups)):
        print(*list(map(lambda x: x.index, groups[i])))
        for e in edges[i]:
            print(*e)


N, M, Q, L, W = li()
G = li()
city_list = []
for i in range(N):
    city_list.append(City(i, *li()))

line_size = 10
area_dict = defaultdict(list)
for city in city_list:
    mean = city.mean()
    key = mean[0] // 1000 * line_size + mean[1] // 1000
    area_dict[key].append(city)

sorted_city_list: list[City] = []
for i in range(line_size):
    if i % 2 == 0:
        # 上から
        sj = 0
        ej = line_size
        dj = 1
    else:
        # 下から
        sj = line_size - 1
        ej = -1
        dj = -1
    for j in range(sj, ej, dj):
        key = i * line_size + j
        sorted_city_list.extend(area_dict[key])

groups: list[list[City]] = []
start_idx = 0
for g in G:
    groups.append(sorted_city_list[start_idx: start_idx + g])
    start_idx += g

# get edges from queries
edges = []
for k in range(M):
    edges.append([])
    for i in range(0, G[k] - 1, L - 1):
        if i < G[k] - (L - 1):
            ret = query(groups[k][i: i + L])
            edges[k].extend(ret)
        else:
            edges[k].extend(query(groups[k][i: G[k]]))

# output answer
answer(groups, edges)
