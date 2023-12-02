import re

digits = "0123456789"

with open("./input.txt", "r") as fp:
    data = fp.readlines()

line_sum = 0
for line in data:
    line_reversed = reversed(line)
    for char in line:
        if char in digits:
            first = char
            break

    for char in line_reversed:
        if char in digits:
            last = char
            break

    line_number = int(f"{first}{last}")
    line_sum += line_number

print(line_sum)
