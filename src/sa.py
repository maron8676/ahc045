import math
import sys
from collections import defaultdict
from sys import stdin

readline = stdin.readline


class City:
    def __init__(self, index: int, lx: int, rx: int, ly: int, ry: int):
        self.index = index
        self.lx = lx
        self.rx = rx
        self.ly = ly
        self.ry = ry

    def __str__(self):
        return f"City[{self.index}, {self.mean()}]"

    def mean(self):
        return [(self.lx + self.rx) // 2, (self.ly + self.ry) // 2]


class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n
        self.group_count_helper = n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        # グループidをメンバー最小値に限定しないようにして多少速くする際にコメントアウト
        if x > y:
            x, y = y, x
        # グループidをメンバー最小値に限定しないようにして多少速くする際にコメント外す
        # if self.parents[x] > self.parents[y]:
        #     x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x
        self.group_count_helper -= 1

    def size(self, x):
        return -self.parents[self.find(x)]

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return self.group_count_helper

    def all_group_members(self):
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find(member)].append(member)
        return group_members

    def __str__(self):
        return '\n'.join(f'{r}: {m}' for r, m in self.all_group_members().items())


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


def calc_dis(city1: City, city2: City) -> float:
    pos1 = city1.mean()
    pos2 = city2.mean()
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


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
        reverse = False
    else:
        # 下から
        sj = line_size - 1
        ej = -1
        dj = -1
        reverse = True
    for j in range(sj, ej, dj):
        key = i * line_size + j
        sorted_city_list.extend(
            sorted(area_dict[key],
                   key=lambda city: city.mean()[1], reverse=reverse))

groups: list[list[City]] = []
start_idx = 0
for g in G:
    groups.append(sorted_city_list[start_idx: start_idx + g])
    start_idx += g

# get edges from queries
edges = []

# 位置が正しいと仮定して解析的に辺を作成する
for group in groups:
    edge = []

    edge_candidate_list = []
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            edge_candidate_list.append((calc_dis(group[i], group[j]), i, j))
    edge_candidate_list.sort(key=lambda x: x[0])

    index_map = {i: v.index for i, v in enumerate(group)}
    uf = UnionFind(len(group))
    for edge_candidate in edge_candidate_list:
        u = edge_candidate[1]
        v = edge_candidate[2]
        if not uf.same(u, v):
            edge.append([index_map[u], index_map[v]])
            uf.union(u, v)
        if uf.group_count() == 1:
            break

    edges.append(edge)

# 1秒焼く

# output answer
answer(groups, edges)
