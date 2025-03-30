from __future__ import annotations

import math
import random
import sys
import time
from collections import defaultdict
from sys import stdin

readline = stdin.readline
start_time = time.time()


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

    def get_bbox(self) -> BBox:
        return BBox(self.lx, self.rx, self.ly, self.ry)


class BBox:
    def __init__(self, lx, rx, ly, ry):
        self.lx = lx
        self.rx = rx
        self.ly = ly
        self.ry = ry

    def intersection(self, other_bbox: BBox) -> BBox:
        x_overlap = [max(self.lx, other_bbox.lx), min(self.rx, other_bbox.rx)]
        y_overlap = [max(self.ly, other_bbox.ly), min(self.ry, other_bbox.ry)]
        return BBox(*x_overlap, *y_overlap)

    def is_collision(self, other_bbox: BBox) -> bool:
        x_overlap = max(self.lx, other_bbox.lx) < min(self.rx, other_bbox.rx)
        y_overlap = max(self.ly, other_bbox.ly) < min(self.ry, other_bbox.ry)
        return x_overlap and y_overlap

    def union(self, other_bbox: BBox):
        self.lx = min(self.lx, other_bbox.lx)
        self.rx = max(self.rx, other_bbox.rx)
        self.ly = min(self.ly, other_bbox.ly)
        self.ry = max(self.ry, other_bbox.ry)


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


def calc_dis(city1: City, city2: City) -> int:
    pos1 = city1.mean()
    pos2 = city2.mean()
    return math.floor(math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2))


def calc_bbox(group: list[City]):
    assert len(group) > 0, "bbox error: empty city list"
    result = group[0].get_bbox()
    for i in range(1, len(group)):
        other_bbox = group[i].get_bbox()
        result.union(other_bbox)
    return result


def calc_cost(city_list: list[City], edges: list[list[int]]) -> int:
    cost = 0

    city_dict = dict()
    for city in city_list:
        city_dict[city.index] = city

    for edge in edges:
        u = city_dict[edge[0]]
        v = city_dict[edge[1]]
        dis = calc_dis(u, v)
        cost += dis

    return cost


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


def cons_minimum_tree(group: list[City]):
    edge = []
    edge_candidate_list: list[tuple[float, int, int]] = []
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

    return edge


# 位置が正しいと仮定して解析的に辺を作成する
for group in groups:
    edge = cons_minimum_tree(group)
    edges.append(edge)

# 1秒焼く
sa_count = 0
T = 1.0
while time.time() - start_time < 1.0:
    sa_count += 1

    source_index = random.randint(0, len(groups) - 1)
    source_group = groups[source_index]

    source_bbox = calc_bbox(source_group)

    target_index = random.randint(0, len(groups) - 1)
    if source_index == target_index:
        continue

    target_group = groups[target_index]
    target_bbox = calc_bbox(groups[target_index])
    if not source_bbox.is_collision(target_bbox):
        continue

    # intersection = source_bbox.intersection(target_bbox)

    # source_indices = [index for index, city in enumerate(source_group)
    #                   if city.get_bbox().is_collision(intersection)]
    # target_indices = [index for index, city in enumerate(target_group)
    #                   if city.get_bbox().is_collision(intersection)]
    #
    # if len(source_indices) == 0 or len(target_indices) == 0:
    #     continue

    before_source_cost = calc_cost(source_group, edges[source_index])
    before_target_cost = calc_cost(target_group, edges[target_index])
    before_cost = before_source_cost + before_target_cost

    # swap
    s1 = random.choice(list(range(len(source_group))))
    s2 = random.choice(list(range(len(target_group))))

    temp = source_group.pop(s1)
    source_group.append(target_group.pop(s2))
    target_group.append(temp)

    # 最小全域木を再計算して、辺の長さの和を比較する
    after_source_edges = cons_minimum_tree(source_group)
    after_target_edges = cons_minimum_tree(target_group)
    after_source_cost = calc_cost(source_group, after_source_edges)
    after_target_cost = calc_cost(target_group, after_target_edges)
    after_cost = after_source_cost + after_target_cost

    # 採用するか判定
    # if random.random() < math.exp(max(min((before_cost - after_cost) / max(float(T), 0.0001), 1), -20)):
    if before_cost - after_cost > 0:
        edges[source_index] = after_source_edges
        edges[target_index] = after_target_edges
    else:
        temp = source_group.pop(len(source_group) - 1)
        source_group.append(target_group.pop(len(target_group) - 1))
        target_group.append(temp)

    T -= 0.0001

# output answer
answer(groups, edges)

print(sa_count, time.time() - start_time, file=sys.stderr)
