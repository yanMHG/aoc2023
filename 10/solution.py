import numpy as np

PIPES = {
    "|": [(-1, 0), (+1, 0)],
    "-": [(0, -1), (0, +1)],
    "L": [(-1, 0), (0, +1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(+1, 0), (0, -1)],
    "F": [(+1, 0), (0, +1)],
    ".": [],
    "S": [],
}


def print_grid_highlight_positions(grid, pos, hi=None):
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if (i, j) in pos:
                if hi is None:
                    print(c, end="")
                else:
                    print(hi, end="")
            else:
                print(".", end="")
        print("")


def read_input(fn: str) -> np.ndarray:
    data = []
    with open(fn, "r") as fp:
        for line in fp:
            row = []
            for char in line.strip():
                row.append(char)
            data.append(row)
    return np.array(data)


def follow_a_position(
    grid: np.ndarray, position: tuple[int, int]
) -> list[tuple[int, int]]:
    curr = grid[position]
    destinations = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            try:
                d = np.array([dx, dy], dtype=int)
                pos = np.array(position, dtype=int)
                dest = grid[tuple(pos + d)]
                if any(d != 0) and all((pos + d) >= 0):
                    d_from_destination = -1 * d
                    if tuple(d_from_destination) in PIPES[dest] and (
                        curr == "S" or tuple(d) in PIPES[curr]
                    ):
                        destinations.append(tuple(pos + d))
            except IndexError:
                pass
    return destinations


def follow_positions(
    grid: np.ndarray, positions: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    output = []
    for pos in positions:
        new_pos = follow_a_position(grid, pos)
        for n in new_pos:
            if n not in output:
                output.append(n)
    return output


def recursive_follow_position(
    grid: np.ndarray, position: tuple[int, int]
) -> tuple[list[tuple[int, int]], np.ndarray]:
    positions = [position]
    accum = positions

    dist_grid = np.empty_like(prototype=grid, dtype=int)
    dist_grid.fill(-1)

    this_dist = 1
    while True:
        positions = follow_positions(grid, positions)
        positions = [p for p in positions if p not in accum]

        for p in positions:
            if dist_grid[p] == -1:
                dist_grid[p] = this_dist

        if len(positions) == 0:
            print_grid_highlight_positions(grid, accum)
            break
        else:
            accum += positions
            this_dist += 1
    return accum, dist_grid


def is_inside(
    grid: np.ndarray, loop: list[tuple[int, int]], pos: tuple[int, int], debug=False
):
    if pos in loop:
        raise ValueError("Choose point outside loop.")

    Y = grid.shape[1]

    y = pos[1]
    n_hits = 0
    last = None
    while y < Y:
        probe = (pos[0], y)
        # if debug:
        #     breakpoint()

        if probe in loop:
            if grid[probe] == "|":
                n_hits += 1
            else:
                if last == "L" and grid[probe] == "7":
                    n_hits += 1
                if last == "F" and grid[probe] == "J":
                    n_hits += 1
                if grid[probe] in ["L", "F"]:
                    last = grid[probe]
        # if debug:
        #     breakpoint()
        y += 1
    if debug:
        breakpoint()
    if n_hits % 2 == 0:
        return False
    else:
        return True


grid = read_input("./input.txt")

S_pos = list(zip(*np.where(grid == "S")))
if len(S_pos) == 1:
    S_pos = S_pos[0]
else:
    raise ValueError

# NOTE: This is particular to my problem
grid[S_pos] = "|"

pos, dists = recursive_follow_position(grid, S_pos)
print(f"Max dist = {dists.max()}")

s = 0
inside = []
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        if (i, j) not in pos and is_inside(grid=grid, loop=pos, pos=(i, j)):
            inside.append((i, j))
            s += 1
print_grid_highlight_positions(grid=grid, pos=inside, hi="I")
print("Inside =", s)
