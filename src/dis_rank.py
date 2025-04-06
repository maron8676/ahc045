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

    def __repr__(self):
        return str(self.index)

    def mean(self):
        return [(self.lx + self.rx) // 2, (self.ly + self.ry) // 2]

    def get_bbox(self) -> BBox:
        return BBox(self.lx, self.rx, self.ly, self.ry)

    def get_width(self):
        return max(self.rx - self.lx, self.ry - self.ly)


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
    # print("query", list(map(str, c)), file=sys.stderr)
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


def calc_dis_range(city1: City, city2: City) -> list[int]:
    if city1.get_bbox().is_collision(city2.get_bbox()):
        min_dis = 1
    elif max(city1.lx, city2.lx) <= min(city1.rx, city2.rx):
        min_dis = min(abs(city1.ry - city2.ly), abs(city1.ly - city2.ry))
    elif max(city1.ly, city2.ly) <= min(city1.ry, city2.ry):
        min_dis = min(abs(city1.rx - city2.lx), abs(city1.lx - city2.rx))
    else:
        min_dis = min(abs(city1.rx - city2.lx) + abs(city1.ry - city2.ly),
                      abs(city2.rx - city1.lx) + abs(city2.ry - city1.ly),
                      abs(city1.rx - city2.lx) + abs(city1.ly - city2.ry),
                      abs(city2.rx - city1.lx) + abs(city2.ly - city1.ry))

    max_dis = max(abs(city1.rx - city2.lx) + abs(city1.ry - city2.ly),
                  abs(city2.rx - city1.lx) + abs(city2.ry - city1.ly),
                  abs(city1.rx - city2.lx) + abs(city1.ly - city2.ry),
                  abs(city2.rx - city1.lx) + abs(city2.ly - city1.ry))

    return [min_dis, max_dis, calc_dis(city1, city2)]


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


def cons_minimum_tree(group: list[City]):
    edge = []
    edge_candidate_list: list[tuple[float, int, int]] = []
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            if (group[i].index, group[j].index) in dis_range_dict:
                edge_candidate_list.append((dis_range_dict[(group[i].index, group[j].index)][2], i, j))
                assert dis_range_dict[(group[i].index, group[j].index)][2] == calc_dis(group[i], group[j]), "wrong dis"
            else:
                edge_candidate_list.append((calc_dis(group[i], group[j]), i, j))
    edge_candidate_list.sort(key=lambda x: x[0])
    index_map = {i: v.index for i, v in enumerate(group)}
    uf = UnionFind(len(group))
    for edge_candidate in edge_candidate_list:
        u = edge_candidate[1]
        v = edge_candidate[2]
        if not uf.same(u, v):
            edge.append(sorted([index_map[u], index_map[v]]))
            uf.union(u, v)
        if uf.group_count() == 1:
            break

    return edge


def exec_sa():
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
    return sa_count


N, M, Q, L, W = li()
G = li()
city_list = []
city_dict = dict()
for i in range(N):
    source_city = City(i, *li())
    city_list.append(source_city)
    city_dict[i] = source_city

line_size = 10
area_dict = defaultdict(list)
for source_city in city_list:
    mean = source_city.mean()
    key = mean[0] // (10000 // line_size) * line_size + mean[1] // (10000 // line_size)
    area_dict[key].append(source_city)

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
sorted_G = sorted(G, reverse=True)
start_idx = 0
for g in sorted_G:
    groups.append(sorted_city_list[start_idx: start_idx + g])
    start_idx += g

dis_range_dict = dict()
dis_range_list = []
for i in range(N):
    for j in range(i + 1, N):
        city_i = city_list[i]
        city_j = city_list[j]
        dis_range = calc_dis_range(city_i, city_j)
        if dis_range[0] < 2000:
            dis_range_dict[(i, j)] = dis_range
            dis_range_list.append(dis_range)

min_max_dis = {i: math.floor(10000 * math.sqrt(2)) for i in range(N)}
items = list(dis_range_dict.items())
items.sort(key=lambda x: x[1][1])

# get edges from queries
edges = []
# 位置が正しいと仮定して解析的に辺を作成する
for group in groups:
    edge = cons_minimum_tree(group)
    edges.append(edge)

sa_count = 0

# 1秒焼く
# sa_count = exec_sa()

# for group in groups:
#     print(group, file=sys.stderr)

# 幅が大きい都市周辺を占って、道路を更新
query_history = set()
group_index = 0
city_index = 0
fortune_index_set = set()
modify_num = 0
while len(query_history) < Q and group_index < len(groups):
    group = groups[group_index]

    edge = edges[group_index]
    edge_dict = defaultdict(list)
    for e in edge:
        edge_dict[e[0]].append(e[1])
        edge_dict[e[1]].append(e[0])

    source_city = group[city_index]
    if (source_city.get_width() < W // 2) and len(edge_dict[source_city.index]) < 3 or len(group) <= 2:
        city_index += 1
        if city_index >= len(group):
            city_index = 0
            group_index += 1
        continue
    if source_city.index in fortune_index_set:
        city_index += 1
        if city_index >= len(group):
            city_index = 0
            group_index += 1
        continue

    # 正確ではないため占いする
    query_edges = set()
    query_cities = [source_city]
    fortune_index_set.add(source_city.index)
    # fortune_index_set.update(edge_dict[source_city.index])
    query_queue = [source_city]
    seen_city = {source_city.index}
    while len(query_queue) > 0 and len(query_cities) < L:
        city = query_queue.pop(0)
        for neighbor in edge_dict[city.index]:
            if neighbor not in seen_city:
                query_edges.add(tuple(sorted([city.index, neighbor])))
                query_cities.append(city_dict[neighbor])
                if len(query_cities) >= L:
                    break
                query_queue.append(city_dict[neighbor])
                seen_city.add(neighbor)

    query_cities.sort(key=lambda x: x.index)
    if tuple(map(lambda x: x.index, query_cities)) in query_history:
        city_index += 1
        if city_index >= len(group):
            city_index = 0
            group_index += 1
        continue

    # print(group_index, city_index, edge, source_city, file=sys.stderr)
    query_result_set = set(query(query_cities))
    query_history.add(tuple(map(lambda x: x.index, query_cities)))
    # print(query_edges, query_result_set, file=sys.stderr)
    remove_edge = []
    add_edge = []
    for e in query_edges:
        if e not in query_result_set:
            remove_edge.append(e)
    for e in query_result_set:
        if e not in query_edges:
            add_edge.append(e)
    for e in remove_edge:
        try:
            edge.remove(list(e))
            modify_num += 1
        except ValueError as exp:
            print(edge, e, file=sys.stderr)
            raise exp
    for e in add_edge:
        edge.append(list(e))

    # dis_rankを更新する
    query_cities_dict = dict()
    for i, city in enumerate(query_cities):
        query_cities_dict[city.index] = i
    query_result_list = list(query_result_set)
    for e in query_result_list:
        uf = UnionFind(len(query_cities))
        for e2 in query_result_list:
            if e == e2:
                continue
            uf.union(query_cities_dict[e2[0]], query_cities_dict[e2[1]])

        uf_groups = uf.all_group_members()
        index1 = query_cities_dict[e[0]]
        group1 = uf_groups[uf.find(index1)]

        index2 = query_cities_dict[e[1]]
        group2 = uf_groups[uf.find(index2)]
        if e == (213, 479):
            print(uf_groups, uf.find(index1), uf.find(index2), file=sys.stderr)

        if e not in dis_range_dict:
            continue
        dis_range = dis_range_dict[e]
        max_dis = 20000
        for city in group2:
            key = tuple(sorted([e[0], query_cities[city].index]))
            if key not in dis_range_dict:
                continue
            max_dis = min(max_dis, dis_range_dict[key][1])
            dis_range_dict[key][0] = max(dis_range[0] + 1, dis_range_dict[key][0])
        for city in group1:
            key = tuple(sorted([e[1], query_cities[city].index]))
            if key not in dis_range_dict:
                continue
            max_dis = min(max_dis, dis_range_dict[key][1])
            dis_range_dict[key][0] = max(dis_range[0] + 1, dis_range_dict[key][0])
        dis_range[1] = min(dis_range[1], max_dis)

    city_index += 1
    if city_index >= len(group):
        city_index = 0
        group_index += 1

# output answer
# group sort
group_dict = defaultdict(list)
for i, group in enumerate(groups):
    group_dict[len(group)].append(i)

answer_groups = []
answer_edges = []
for g in G:
    index = group_dict[g].pop()
    answer_groups.append(groups[index])
    answer_edges.append(edges[index])

answer(answer_groups, answer_edges)

print(len(query_history), modify_num, time.time() - start_time, file=sys.stderr)
print(items[:10], file=sys.stderr)
print(len(dis_range_dict), file=sys.stderr)

for edge in edges:
    if len(edge) == 0:
        continue
    for e in edge:
        if tuple(e) in dis_range_dict:
            print(e, dis_range_dict[tuple(e)], city_list[e[0]].mean(), city_list[e[1]].mean(), file=sys.stderr)
        else:
            print(e, calc_dis_range(city_list[e[0]], city_list[e[1]]), city_list[e[0]].mean(), city_list[e[1]].mean(),
                  file=sys.stderr)
    print(file=sys.stderr)
