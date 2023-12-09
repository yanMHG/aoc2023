import numpy as np


def read_input(fn: str) -> list[int]:
    data = []
    with open(fn, "r") as fp:
        for line in fp:
            d = []
            for num in line.split():
                d.append(int(num))
            data.append(d)
    return data


def predict_forward(seq: list[int]) -> int:
    diffs = np.array(seq)
    next_element = diffs[-1]
    while not np.all(diffs == 0):
        diffs = np.diff(diffs)
        next_element += diffs[-1]
    return next_element


def predict_backward(seq: list[int]) -> int:
    diffs = np.array(seq)
    power_of_one = 0
    next_element = ((-1) ** power_of_one) * diffs[0]
    while not np.all(diffs == 0):
        diffs = np.diff(diffs)
        power_of_one += 1
        next_element += ((-1) ** power_of_one) * diffs[0]
    return next_element


data = read_input("./input.txt")

print(sum(predict_forward(d) for d in data))
print(sum(predict_backward(d) for d in data))
