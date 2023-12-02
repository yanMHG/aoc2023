import re

digits = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


with open("./input.txt", "r") as fp:
    data = fp.readlines()


def get_first_digit(line: str) -> str:
    s = len(line)
    for i in range(s):
        substr = line[i:]
        for digit in digits:
            if substr.find(digit) == 0:
                return digits[digit]


def get_last_digit(line: str) -> str:
    s = len(line)
    for i in range(s):
        substr = line[-1 - i : -1]
        for digit in digits:
            if substr.find(digit) == 0:
                return digits[digit]


line_sum = 0
for line in data:
    first = get_first_digit(line)
    last = get_last_digit(line)
    line_number = int(f"{first}{last}")
    line_sum += line_number
print(line_sum)
