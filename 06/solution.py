import numpy as np


def number_of_ways(total_time: int, record: int) -> int:
    return (
        # Strict Floor
        1
        - np.floor(-(-total_time + np.sqrt(total_time**2 - 4 * record)) / 2)
        # Strict Ceil
        - 1
        + np.ceil(-(-total_time - np.sqrt(total_time**2 - 4 * record)) / 2)
        - 1
    )


def part_one_parse() -> tuple[list, list]:
    with open("./input.txt", "r") as fp:
        data = fp.readlines()
    times = [int(t) for t in data[0].split()[1:]]
    records = [int(r) for r in data[1].split()[1:]]
    return times, records


def part_two_parse() -> tuple[int, int]:
    with open("./input.txt", "r") as fp:
        data = fp.readlines()
    time = int("".join(data[0].split()[1:]))
    record = int("".join(data[1].split()[1:]))
    return time, record


# Part One
times, records = part_one_parse()
print(
    np.product(
        [
            number_of_ways(total_time=time, record=record)
            for time, record in zip(times, records)
        ]
    )
)

# Part Two
time, record = part_two_parse()
print(number_of_ways(total_time=time, record=record))
