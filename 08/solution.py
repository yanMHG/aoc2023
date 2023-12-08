import math
import re
from dataclasses import dataclass


@dataclass
class Node:
    label: str
    left: str
    right: str


def parse_input(fn: str) -> tuple[str, dict[str, Node]]:
    nodes = {}
    with open(fn, "r") as fp:
        for i, line in enumerate(fp):
            if i == 0:
                directions = line.strip()
            if i > 1:
                parse = re.search(
                    "([A-Z0-9]{3}) = \\(([A-Z0-9]{3}), ([A-Z0-9]{3})\\)", line
                )
                nodes[parse.group(1)] = Node(
                    label=parse.group(1), left=parse.group(2), right=parse.group(3)
                )
    return directions, nodes


def walk_graph(directions: str, nodes: dict[str, Node]) -> int:
    route = []
    node = nodes["AAA"]
    # route.append(node)
    i = 0
    while True:
        direction = directions[i % len(directions)]
        if direction == "L":
            node = nodes[node.left]
        else:
            node = nodes[node.right]
        # route.append(node)
        i += 1
        if node.label == "ZZZ":
            break
    return i


def simultaneous_walk_graph(directions: str, nodes: dict[str, Node]) -> int:
    route = []
    node = tuple([node for node in nodes.values() if node.label.endswith("A")])
    # route.append(node)
    i = 0
    ended = {}
    while True:
        direction = directions[i % len(directions)]
        if direction == "L":
            node = tuple([nodes[n.left] for n in node])
        else:
            node = tuple([nodes[n.right] for n in node])
        # route.append(node)
        i += 1
        for j, n in enumerate(node):
            if n.label.endswith("Z"):
                if j not in ended:
                    ended[j] = i
        if len(ended) == len(node):
            break
    return math.lcm(*list(ended.values()))


directions, nodes = parse_input("./input.txt")

print(walk_graph(directions, nodes))
print(simultaneous_walk_graph(directions, nodes))
