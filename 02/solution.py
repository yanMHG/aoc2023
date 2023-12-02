from dataclasses import dataclass


@dataclass
class Hand:
    red: int
    green: int
    blue: int

    @classmethod
    def from_string(cls, string: str) -> "Hand":
        hand = {"red": 0, "green": 0, "blue": 0}
        sp = string.split(", ")
        for s in sp:
            amount, color = s.split()
            hand[color] = int(amount)
        return Hand(red=hand["red"], green=hand["green"], blue=hand["blue"])

    def is_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
        if self.red <= max_red and self.green <= max_green and self.blue <= max_blue:
            return True
        return False

    def power(self) -> int:
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    hands: list[Hand]

    @classmethod
    def from_string(cls, string: str) -> "Game":
        game = []
        id, hand_strings = string.split(": ")
        for hand_string in hand_strings.split("; "):
            hand = Hand.from_string(hand_string)
            game.append(hand)
        return Game(id=int(id.split()[-1]), hands=game)

    def is_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
        for hand in self.hands:
            if not hand.is_possible(
                max_red=max_red, max_green=max_green, max_blue=max_blue
            ):
                return False
        return True

    def max_hand(self) -> Hand:
        maxes = {}
        for color in "red", "green", "blue":
            maxes[color] = max([getattr(hand, color) for hand in self.hands])
        return Hand(**maxes)


with open("./input.txt", "r") as fp:
    data = fp.readlines()


id_sum = 0
power_sum = 0
for game_string in data:
    game = Game.from_string(game_string)
    if game.is_possible(max_red=12, max_green=13, max_blue=14):
        id_sum += game.id
    power_sum += game.max_hand().power()

print("Part One:", id_sum)
print("Part Two:", power_sum)
