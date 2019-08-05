'''
Implementation of the AI poker player.
'''

from evaluatorTest import *
from playerModel import *
from objects import *

from datetime import datetime
import copy
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

    def getPlayerScores(self):
        player_scores = []
        open_cards_as_lists = copy.deepcopy(self.open_cards)
        for i in range(len(open_cards_as_lists)):
            open_cards_as_lists[i] = [open_cards_as_lists[i].rank, open_cards_as_lists[i].suit]

        for i in range(NUM_OF_PLAYERS):
            if self.players_in_round[i]:
                player_hand = copy.deepcopy(open_cards_as_lists)
                player_cards_as_cards = self.player_cards[i]
                player_hand.append([player_cards_as_cards[0].rank, player_cards_as_cards[0].suit])
                player_hand.append([player_cards_as_cards[1].rank, player_cards_as_cards[1].suit])
                player_scores.append(getHandScore(player_hand))
            else:
                player_scores.append(0)

        return player_scores

    def getWinners(self, player_scores):
        max_val = 0
        winners = []

        for i in range(len(player_scores)):
            if player_scores[i] > max_val and self.players_in_round[i]:
                max_val = player_scores[i]
                winners = [[i,self.player_bets[i]]]
            elif player_scores[i] == max_val and self.players_in_round[i]:
                winners.append([i,self.player_bets[i]])

        return winners

    def getWinnerGroups(self, winners):
        winner_groups = []
        winners_sorted_by_pot_size = sorted(winners, key=lambda x: x[1])

        current_winner_pot_size = winners_sorted_by_pot_size[0][1]
        current_group = [winners_sorted_by_pot_size[0]]
        for j in range(len(winners_sorted_by_pot_size) - 1):
            i = j + 1
            if winners_sorted_by_pot_size[i][1] == current_winner_pot_size:
                current_group.append(winners_sorted_by_pot_size[i])
            else:
                winner_groups.append(current_group)
                current_group = [winners_sorted_by_pot_size[i]]
        winner_groups.append(current_group)

        return winner_groups

    def giveWinningsToWinners(self, winners):
        winner_ids = [item[0] for item in winners]
        winner_groups = self.getWinnerGroups(winners)

        for winner_group in winner_groups:
            winner_ids_in_group = [item[0] for item in winner_group]
            for winner_id in winner_ids_in_group:
                # Give winnings to first group
                for i in range(len(self.player_bets)):
                    if i not in winner_ids and self.player_bets[i] > 0:
                        value_transferred = self.player_bets[i] / len(winners)
                        self.player_stacks[i] -= value_transferred
                        self.player_bets[i] -= value_transferred
                        self.player_stacks[winner_id] += value_transferred
                self.player_bets[winner_id] = 0.0

    def divideSpoils(self):
        # TODO:: make sure you test this
        player_scores = self.getPlayerScores()

        did_clean_all_players = False
        while not did_clean_all_players:
            winners = self.getWinners(player_scores)

            self.giveWinningsToWinners(winners)
            did_clean_all_players = (sum(self.player_bets) == 0)

        print()
        '''for winner_group in winner_groups:
            for winner in winner_group:
                for i in range(len(self.player_bets)):
                    if i not in winner_ids:
                        value_transferred = self.player_bets[winner[1]] / len(winners)
                        self.player_stacks[i] -= value_transferred
                        self.player_stacks[winner[0]] += value_transferred'''

        #for i in range(len(self.player_bets)):
        #    self.player_stacks[i] -= self.player_bets[i]

        #prize_per_winner = self.pot_size / len(winners)

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
        if len(self.open_cards) == 0:
            print("[]")
        for i in range(len(self.open_cards)):
            print(self.open_cards[i].getString())

        print("Player cards:")
        for i in range(len(self.player_cards)):
            cards = self.player_cards[i]
            print("Player " + str(i) + ". Cards: " + cards[0].getString() + ", " + cards[1].getString())
        print("Last raiser: " + str(self.last_raiser))

def testWinningFunctions():
    table = Table()
    # TODO:: implement

    #table.

if __name__ == '__main__':
    testWinningFunctions()

    table = Table()
    player_model = PlayerModel()
    table.print()
    table.runGame()

    # Currently allows about 13,000 hand scorings per second. If turns out to be a bottleneck will improve later.
    '''print(datetime.now())
    for i in range(50000):
        testHands()
    print(datetime.now())'''