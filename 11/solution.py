import numpy as np


def read_input(fn):
    data = []
    with open(fn, "r") as fp:
        for line in fp:
            d = []
            for char in line.strip():
                d.append(char)
            data.append(d)
    return np.array(data)


def expand_universe(universe):
    rows = []
    for i, row in enumerate(universe):
        if np.all(row == "."):
            rows.append(i)
    cols = []
    for j, col in enumerate(universe.T):
        if np.all(col == "."):
            cols.append(j)

    expanded_universe = universe.copy()
    delta = 0
    for i in rows:
        expanded_universe = np.insert(
            arr=expanded_universe, obj=i + delta, values=".", axis=0
        )
        delta += 1
    delta = 0
    for j in cols:
        expanded_universe = np.insert(
            arr=expanded_universe, obj=j + delta, values=".", axis=1
        )
        delta += 1
    return expanded_universe


def distance(galaxy_1, galaxy_2):
    dist = sum(np.abs(galaxy_2[i] - galaxy_1[i]) for i in range(len(galaxy_1)))
    return dist


def pairwise_distances(galaxies, expand_factor):
    rows = []
    for i, row in enumerate(universe):
        if np.all(row == "."):
            rows.append(i)
    cols = []
    for j, col in enumerate(universe.T):
        if np.all(col == "."):
            cols.append(j)

    G = len(galaxies)
    S = 0
    for i in range(G):
        for j in range(G):
            if j > i:
                S += distance(galaxies[i], galaxies[j])
                # space expansion correction
                min_X = min((galaxies[i][0], galaxies[j][0]))
                max_X = max((galaxies[i][0], galaxies[j][0]))
                min_Y = min((galaxies[i][1], galaxies[j][1]))
                max_Y = max((galaxies[i][1], galaxies[j][1]))
                # now check how many repeated rows and cols lie in the way
                n_rows = len([r for r in rows if r > min_X and r < max_X])
                n_cols = len([c for c in cols if c > min_Y and c < max_Y])
                if n_rows > 0:
                    S += n_rows * (expand_factor - 1)
                if n_cols > 0:
                    S += n_cols * (expand_factor - 1)
    return S


universe = read_input("./input.txt")

galaxies = list(zip(*np.where(universe == "#")))

print(pairwise_distances(galaxies, expand_factor=2))
print(pairwise_distances(galaxies, expand_factor=1000000))
