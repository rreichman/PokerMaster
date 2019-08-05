'''
Implementation of the AI poker player.
'''

from evaluatorTest import *
from playerModel import *

from datetime import datetime

import random

INITIAL_STACK_SIZE = 1500
NUM_OF_PLAYERS = 6

class Table(object):
    def __init__(self):
        self.deck = Deck()

        self.player_stacks = [INITIAL_STACK_SIZE] * NUM_OF_PLAYERS
        self.player_bets = [0] * NUM_OF_PLAYERS
        self.players_in_round = [True] * NUM_OF_PLAYERS
        self.number_of_players_in_round = NUM_OF_PLAYERS
        self.open_cards = []
        # Assuming here that ego is always in position 0
        self.dealer_position = random.randint(0, 5)
        self.player_cards = self.deck.dealCards(number_of_players=6)

        self.big_blind_size = INITIAL_STACK_SIZE / 50
        self.player_bets[self.dealer_position] = self.big_blind_size / 2
        self.player_bets[(self.dealer_position + 1) % NUM_OF_PLAYERS] = self.big_blind_size
        self.last_raiser = (self.dealer_position + 1) % NUM_OF_PLAYERS

        self.highest_bet = self.big_blind_size
        self.pot_size = self.big_blind_size * 3 / 2

        # TODO:: in the future maybe handle cases where players leave the table
        self.current_player_index = (self.dealer_position + 2) % NUM_OF_PLAYERS

    def runGame(self):
        self.print()
        self.runRound()
        if self.number_of_players_in_round > 1:
            for i in range(3):
                self.open_cards.append(self.deck.pop())
            self.runRound()
            if self.number_of_players_in_round > 1:
                self.open_cards.append(self.deck.pop())
                self.runRound()
                if self.number_of_players_in_round > 1:
                    self.open_cards.append(self.deck.pop())
                    self.runRound()

    def runRound(self):
        self.endRound = False
        while not self.endRound:
            table.getAction(player_model.act(table))
            table.print()

        if len(self.open_cards) == 5:
            self.divideSpoils()

    def divideSpoils(self):
        # TODO:: this is a bit complex, make sure you do it right.
        winners = self.getWinners()
        for i in range(len(self.player_bets)):
            self.player_stacks[i] -= self.player_bets[i]

        prize_per_winner = self.pot_size / len(winners)

    def getAction(self, action):
        action_string = "\nPlayer " + str(self.current_player_index) + " played " + action.type

        if action.type == "Raise":
            # TODO:: maybe make sure that the bet is legal
            action_string += ", value: " + str(action.value)
            self.player_bets[self.current_player_index] = self.highest_bet + action.value
            self.highest_bet = self.player_bets[self.current_player_index]
            self.last_raiser = self.current_player_index
        else:
            if self.last_raiser == self.getNextPlayerIndex():
                self.endRound = True
            if action.type == "Check":
                self.player_bets[self.current_player_index] = self.highest_bet
            elif action.type == "Fold":
                self.players_in_round[self.current_player_index] = False
                self.number_of_players_in_round -= 1

        self.current_player_index = self.getNextPlayerIndex()

        self.pot_size = 0
        for i in range(len(self.player_bets)):
            self.pot_size += self.player_bets[i]

        print(action_string)

    def getNextPlayerIndex(self):
        next_player_index = self.current_player_index
        while True:
            next_player_index = (next_player_index + 1) % NUM_OF_PLAYERS
            if self.players_in_round[next_player_index]:
                return next_player_index

    def moveRaise(self, player_index, value):
        self.player_bets[player_index] += value

    def print(self):
        print("Dealer position: " + str(self.dealer_position))
        print("Player bets:")
        print(self.player_bets)
        print("Players in round:")
        print(self.players_in_round)
        print("Pot size: " + str(self.pot_size))
        print("\nOpen cards:")
        open_cards_string = ""
        if len(self.open_cards) == 0:
            open_cards_string = "[]"
        for i in range(len(self.open_cards)):
            open_cards_string += self.open_cards[i].getString() + ","
        print(open_cards_string)
        #for i in range(len(self.player_cards))
        print("Player cards:")
        for i in range(len(self.player_cards)):
            cards = self.player_cards[i]
            print("Player " + str(i) + ". Cards: " + cards[0].getString() + ", " + cards[1].getString())
        print("Last raiser: " + str(self.last_raiser))

class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def getString(self):
        return "Rank: " + str(self.rank) + ", Suit: " + str(self.suit)

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
    table = Table()
    player_model = PlayerModel()
    table.print()
    table.runGame()

    # Currently allows about 13,000 hand scorings per second. If turns out to be a bottleneck will improve later.
    '''print(datetime.now())
    for i in range(50000):
        testHands()
    print(datetime.now())'''