from evaluatorTest import *

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

if __name__ == '__main__':
    initial_table = Table()
    #testHands()