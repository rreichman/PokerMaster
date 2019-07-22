from evaluator import *

import random

class Table(object):
    def __init__(self):
        self.deck = Deck()

        INITIAL_STACK_SIZE = 1500

        self.player_stacks = [INITIAL_STACK_SIZE] * 6
        self.player_bets = [0] * 6
        self.open_cards = []
        self.dealer_position = random.randint(0, 5)
        self.player_cards = self.deck.dealCards(number_of_players=6)

class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

class Deck(object):
    def __init__(self):
        self.cards = []
        for i in range(1,14,1):
            for j in range(4):
                self.cards.append(Card(i, j))

    def pop(self):
        card_index = random.randint(0, len(self.cards) - 1)
        card = self.cards[card_index]
        del self.cards[card_index]
        return card

    def dealCards(self, number_of_players):
        player_cards = []
        for player_index in range(number_of_players):
            player_cards.append([self.pop(), self.pop()])

        return player_cards

def getHandScore(hand):
    hand_with_aces_as_fourteens = []
    has_aces = False
    for card in hand:
        if card[0] == 1:
            has_aces = True
            hand_with_aces_as_fourteens.append([14, card[1]])
        else:
            hand_with_aces_as_fourteens.append(card)

    evaluator = HandEvaluator(hand)
    small_aces_score = evaluator.getScore()

    if has_aces:
        evaluator_aces = HandEvaluator(hand_with_aces_as_fourteens)
        large_aces_score = evaluator_aces.getScore()
        return max(small_aces_score, large_aces_score)
    else:
        return small_aces_score

def testStraightFlush():
    straight_flush_preset = VALUE_PRESETS["straight_flush"]

    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]) == straight_flush_preset + 4)
    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 1]]) == straight_flush_preset + 3)
    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 1], [8, 1]]) == straight_flush_preset + 2)
    assert (getHandScore([[6, 0], [3, 0], [4, 0], [5, 0], [7, 0], [7, 1], [8, 1]]) == straight_flush_preset + 3)
    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 1], [7, 1], [8, 1]]) == 4)
    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 1], [7, 1], [1, 1]]) == 4)
    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 1], [7, 1], [1, 0]]) == straight_flush_preset + 1)
    assert (getHandScore([[12, 0], [11, 0], [10, 0], [13, 0], [6, 1], [7, 1], [1, 0]]) == straight_flush_preset + 10)

def testFourOfAKind():
    four_of_a_kind_preset = VALUE_PRESETS["four_of_kind"]

    assert (getHandScore([[2, 0], [2, 1], [2, 2], [2, 3], [11, 0], [7, 1], [8, 0]]) == four_of_a_kind_preset + 11)
    assert (getHandScore([[12, 0], [12, 1], [12, 2], [12, 3], [11, 0], [7, 1], [8, 0]]) == four_of_a_kind_preset + 11)
    assert (getHandScore([[12, 0], [12, 1], [12, 2], [12, 3], [1, 0], [7, 1], [8, 0]]) == four_of_a_kind_preset + 14)
    assert (getHandScore([[12, 0], [12, 1], [12, 2], [12, 3], [2, 0], [7, 1], [8, 0]]) == four_of_a_kind_preset + 8)
    assert (getHandScore([[2, 0], [3, 0], [4, 2], [5, 2], [11, 0], [7, 1], [8, 0]]) == 4)

def testFullHouse():
    full_house_preset = VALUE_PRESETS["full_house"]

    assert (getHandScore([[12, 0], [12, 1], [12, 2], [7, 3], [2, 0], [7, 1], [8, 0]]) == full_house_preset + 120 + 7)
    assert (getHandScore([[2, 0], [2, 1], [12, 2], [7, 3], [2, 0], [7, 1], [8, 0]]) == full_house_preset + 20 + 7)
    assert (getHandScore([[2, 0], [2, 1], [12, 2], [7, 3], [2, 0], [12, 1], [8, 0]]) == full_house_preset + 20 + 12)
    assert (getHandScore([[2, 0], [2, 1], [12, 2], [7, 3], [2, 0], [12, 1], [7, 0]]) == full_house_preset + 20 + 12)
    assert (getHandScore([[2, 0], [2, 1], [3, 2], [7, 3], [2, 0], [3, 1], [7, 0]]) == full_house_preset + 20 + 7)

def testFlush():
    flush_preset = VALUE_PRESETS["flush"]

    assert (getHandScore([[12, 0], [12, 1], [11, 0], [7, 3], [2, 0], [7, 0], [8, 0]]) == flush_preset + 40)
    assert (getHandScore([[12, 0], [12, 1], [11, 0], [7, 3], [1, 0], [7, 0], [8, 0]]) == flush_preset + 52)
    assert (getHandScore([[1, 0], [10, 0], [3, 0], [8, 0], [4, 0], [5, 0], [6, 0]]) == flush_preset + 43)
    assert (getHandScore([[1, 0], [10, 0], [3, 0], [8, 0], [4, 0], [5, 0], [7, 0]]) == flush_preset + 44)

def testHands():
    testStraightFlush()
    testFourOfAKind()
    testFullHouse()
    testFlush()

if __name__ == '__main__':
    initial_table = Table()
    testHands()
    #print(getHandScore([[2, 0], [3, 1], [4, 2], [5, 2], [2, 4], [7, 3], [9, 1]]))