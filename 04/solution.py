with open("./input.txt", "r") as fp:
    data = fp.readlines()

cards = []

part_one_punct = {}
for card in data:
    card_spec, numbers = card.split(":")
    _, card_number = card_spec.split()
    winning, have = numbers.split("|")
    winning = [int(x) for x in winning.split()]
    have = [int(x) for x in have.split()]
    card_number = int(card_number)

    cards.append({"id": card_number, "winning": winning, "have": have})

    card_punct = 0
    for h in have:
        if h in winning:
            card_punct += 1
    if card_punct > 0:
        card_punct = 2 ** (card_punct - 1)
    part_one_punct[card_number] = card_punct

print(sum(part_one_punct.values()))


instances = {k["id"]: 1 for k in cards}
for card in cards:
    id = card["id"]
    nwin = len([x for x in card["have"] if x in card["winning"]])
    for d in range(nwin):
        instances[id + d + 1] += instances[id]


print(sum(instances.values()))
