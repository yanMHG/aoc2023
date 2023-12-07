from enum import Enum
from typing import Union

import numpy as np


class HandType(Enum):
    FiveOfAKind = 1
    FourOfAKind = 2
    FullHouse = 3
    ThreeOfAKind = 4
    TwoPair = 5
    OnePair = 6
    HighCard = 7

    def __int__(self):
        return self.value


def read_input(fn: str) -> tuple[list[str], list[int]]:
    hands = []
    bids = []
    with open(fn, "r") as fp:
        data = fp.readlines()
    for line in data:
        hand, bid = line.split()
        bid = int(bid)
        hands.append(hand)
        bids.append(bid)
    return hands, bids


def get_hand_type(hand: list[str], use_joker=False) -> HandType:
    counts = {}
    for card in hand:
        if card not in counts:
            counts[card] = 1
        else:
            counts[card] += 1

    if use_joker and "J" in hand:
        _max = -1
        _kmax = None
        for k, v in counts.items():
            if k != "J":
                if v > _max:
                    _kmax = k
                    _max = v
        if _kmax is not None:
            counts[_kmax] += counts["J"]
            del counts["J"]

    if len(counts) == 1:
        return HandType.FiveOfAKind
    if len(counts) == 2:
        if 1 in counts.values():
            return HandType.FourOfAKind
        else:
            return HandType.FullHouse
    if len(counts) == 3:
        if 2 in counts.values():
            return HandType.TwoPair
        else:
            return HandType.ThreeOfAKind
    if len(counts) == 4:
        return HandType.OnePair
    if len(counts) == 5:
        return HandType.HighCard
    raise ValueError(f"Unknown hand type for: {hand}")


def card_is_better_than_card(card_1, card_2, use_joker=False) -> Union[bool, None]:
    if use_joker:
        cards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    else:
        cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    i_1 = cards.index(card_1)
    i_2 = cards.index(card_2)
    if i_1 < i_2:
        return True
    if i_2 < i_1:
        return False
    return None


def hand_is_better_than_hand(
    hand_1: list[str], hand_2: list[str], use_joker=False
) -> bool:
    type_1 = get_hand_type(hand_1, use_joker=use_joker)
    type_2 = get_hand_type(hand_2, use_joker=use_joker)

    if int(type_1) < int(type_2):
        return True

    if int(type_2) < int(type_1):
        return False

    # same type
    for card_1, card_2 in zip(hand_1, hand_2):
        comp = card_is_better_than_card(card_1, card_2, use_joker=use_joker)
        if comp is not None:
            return comp
    raise ValueError


def calc_total_winnings(ranks: list[int], bids: list[int]) -> int:
    return np.sum(np.array(ranks, dtype=int) * np.array(bids, dtype=int))


def sort_hands(hands: list[list[str]], use_joker=False) -> list[list[str]]:
    def quicksort(arr):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            left = [
                x
                for x in arr[1:]
                if hand_is_better_than_hand(pivot, x, use_joker=use_joker)
            ]
            right = [
                x
                for x in arr[1:]
                if hand_is_better_than_hand(x, pivot, use_joker=use_joker)
            ]
            return quicksort(left) + [pivot] + quicksort(right)

    return quicksort(hands)


def get_ranks(hands: list[list[str]], use_joker=False) -> list[int]:
    sorted = sort_hands(hands, use_joker=use_joker)
    return [i + 1 for i in [sorted.index(h) for h in hands]]


hands, bids = read_input("./input.txt")

# Part One
ranks = get_ranks(hands)
print(calc_total_winnings(ranks, bids))

# Part Two
ranks = get_ranks(hands, use_joker=True)
print(calc_total_winnings(ranks, bids))
