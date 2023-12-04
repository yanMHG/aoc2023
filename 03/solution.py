import re

import numpy as np


def get_numbers_and_positions(x: np.ndarray) -> list:
    output = []
    for i, row in enumerate(x):
        s = "".join(row)
        m = re.finditer("[0-9]+", s)
        for match in m:
            output.append(
                {
                    "number": int(match.group(0)),
                    "positions": [
                        (i, match.start() + j) for j in range(len(match.group(0)))
                    ],
                }
            )
    return output


def get_gears(x: np.ndarray) -> list:
    I = x.shape[0]
    J = x.shape[1]
    pos = []
    for i in range(I):
        for j in range(J):
            if x[i, j] == "*":
                pos.append((i, j))
    return pos


def get_neighbor_positions(x: np.ndarray, k: tuple) -> list[tuple]:
    initial = []
    for x_disp in [-1, 0, +1]:
        for y_disp in [-1, 0, +1]:
            dx = k[0] + x_disp
            dy = k[1] + y_disp
            if dx >= x.shape[0]:
                dx = x.shape[0] - 1
            if dx < 0:
                dx = 0
            if dy >= x.shape[1]:
                dy = x.shape[1] - 1
            if dy < 0:
                dy = 0
            d = (dx, dy)
            if d not in initial and d != k:
                initial.append(d)
    return initial


def is_symbol_in_neighbors(x: np.ndarray, ks: list[tuple]) -> bool:
    nps = get_union_of_neighbor_positions(x, ks)
    for pos in nps:
        if x[pos] != ".":
            return True
    return False


def get_union_of_neighbor_positions(x: np.ndarray, ks: list[tuple]) -> list[tuple]:
    l = []
    for k in ks:
        l += [n for n in get_neighbor_positions(x, k) if n not in ks]
    return list(set(list(l)))


with open("./input.txt", "r") as fp:
    data = fp.readlines()


for i, line in enumerate(data):
    data[i] = list(line.strip())


data_arr = np.array(data)
numbers = get_numbers_and_positions(data_arr)
gears = get_gears(data_arr)

part_numbers = []
for k in numbers:
    s = is_symbol_in_neighbors(x=data_arr, ks=k["positions"])
    if s:
        part_numbers.append(k)

print(sum(k["number"] for k in part_numbers))

gear_ratios = []
for gear_pos in gears:
    gear_neis = get_neighbor_positions(data_arr, gear_pos)
    nei_part_numbers = []
    for n in part_numbers:
        for n_pos in n["positions"]:
            if n_pos in gear_neis:
                nei_part_numbers.append(n["number"])
                break

    if len(nei_part_numbers) == 2:
        gear_ratios.append(np.product(nei_part_numbers))

print(sum(gear_ratios))
