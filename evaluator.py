import math

POWER_PRESET = 100000000
VALUE_PRESETS = {"straight_flush" : 10 * POWER_PRESET, "four_of_kind" : 9 * POWER_PRESET,
                 "full_house" : 8 * POWER_PRESET, "flush" : 7 * POWER_PRESET, "straight": 6 * POWER_PRESET,
                 "three_of_kind" : 5 * POWER_PRESET, "two_pair" : 4 * POWER_PRESET, "pair" : 3 * POWER_PRESET}


def getHighestCardScore(cards, number_of_cards_to_count):
    sorted_by_rank = sorted(cards, key=lambda x: x[0])

    score = 0
    for i in range(number_of_cards_to_count):
        score += math.pow(20, i) * sorted_by_rank[len(cards) - number_of_cards_to_count + i][0]

    return int(score)

class HandEvaluator(object):
    def __init__(self, cards):
        if len(cards) == 7:
            self.cards = cards
            self.ranks_count, self.suits_count = self.getStatistics(self.cards)
            self.inv_ranks_count = {v: k for k, v in self.ranks_count.items()}
            self.sorted_flush_cards = sorted(self.getFlushValuesIfFlushExists())
        else:
            raise Exception("no point calculating score without all cards on table")

    def getStraightFlushScore(self):
        if len(self.sorted_flush_cards) > 0:
            longest_streak = self.getStraightCardsIfExist(self.sorted_flush_cards)

            if len(longest_streak) >= 5:
                return VALUE_PRESETS["straight_flush"] + self.getXHighestCardScore(longest_streak, 5)

        return 0

    def getFourOfKindScore(self):
        if 4 in self.ranks_count.values():
            four_of_kind_value = self.inv_ranks_count[4]

            cards_without_four_of_kind = []
            for card in self.cards:
                if card[0] != four_of_kind_value:
                    cards_without_four_of_kind.append(card)

            return VALUE_PRESETS["four_of_kind"] + \
                   self.getCardWithXHighestCardScore(cards_without_four_of_kind, number_of_cards_to_count=1)

        return 0

    def getFullHouseScore(self):
        if 3 in self.ranks_count.values() and 2 in self.ranks_count.values():
            rank_appearing_three_times = self.inv_ranks_count[3]
            highest_two_card = 0
            for rank in self.ranks_count:
                rank_appearances = self.ranks_count[rank]
                if rank_appearances == 2 and rank > highest_two_card:
                    highest_two_card = rank

            return VALUE_PRESETS["full_house"] + 20 * rank_appearing_three_times + highest_two_card

        return 0

    def getFlushValuesIfFlushExists(self):
        for suit in self.suits_count:
            if self.suits_count[suit] >= 5:
                flush_cards = []
                for card in self.cards:
                    if card[1] == suit:
                        flush_cards.append(card[0])
                return flush_cards

        return []

    def getFlushScore(self):
        if len(self.sorted_flush_cards) >= 5:
            val = 0
            for i in range(5):
                val += self.sorted_flush_cards[len(self.sorted_flush_cards) - 5 + i]
            return VALUE_PRESETS["flush"] + val

        return 0

    def getStraightCardsIfExist(self, sorted_unique_rank_cards):
        longest_streak = [sorted_unique_rank_cards[0]]

        for i in range(len(sorted_unique_rank_cards) - 1):
            if sorted_unique_rank_cards[i] == sorted_unique_rank_cards[i + 1] - 1:
                longest_streak.append(sorted_unique_rank_cards[i + 1])
            else:
                if len(longest_streak) >= 5:
                    break
                if len(longest_streak) > len(sorted_unique_rank_cards) - i:
                    break
                longest_streak = [sorted_unique_rank_cards[i + 1]]

        return longest_streak

    def getStraightScore(self):
        sorted_unique_ranks = sorted(self.ranks_count.keys())
        straight_cards = self.getStraightCardsIfExist(sorted_unique_ranks)

        if len(straight_cards) >= 5:
            return VALUE_PRESETS["straight"] + self.getXHighestCardScore(straight_cards, 5)

        return 0

    def removeCardsOfGivenValues(self, cards, values):
        cards_without_given_values = []

        for card in self.cards:
            if card[0] not in values:
                cards_without_given_values.append(card)

        return cards_without_given_values

    def getThreeOfKindScore(self):
        if 3 in self.ranks_count.values():
            highest_three_card = 0
            for rank in self.ranks_count:
                rank_appearances = self.ranks_count[rank]
                if rank_appearances == 3 and rank > highest_three_card:
                    highest_three_card = rank

            cards_without_highest_three_card = self.removeCardsOfGivenValues(self.cards, [highest_three_card])

            return VALUE_PRESETS["three_of_kind"] + 10000 * highest_three_card + \
                   getHighestCardScore(cards_without_highest_three_card, 2)

        return 0

    def getTwoPairScore(self):
        number_of_two_pairs = list(self.ranks_count.values()).count(2)
        if number_of_two_pairs >= 2:
            two_pair_list = []
            for rank_count in self.ranks_count:
                if self.ranks_count[rank_count] == 2:
                    two_pair_list.append(rank_count)

            sorted_two_pairs = sorted(two_pair_list, reverse=True)

            cards_without_highest_two_pairs = \
                self.removeCardsOfGivenValues(self.cards,[sorted_two_pairs[0], sorted_two_pairs[1]])

            return VALUE_PRESETS["two_pair"] + 200 * sorted_two_pairs[0] + 10 * sorted_two_pairs[1] + \
                   self.getCardWithXHighestCardScore(cards_without_highest_two_pairs, 1)

        return 0

    def getPairScore(self):
        number_of_pairs = list(self.ranks_count.values()).count(2)
        if number_of_pairs == 1:
            pair_value = self.inv_ranks_count[2]

            cards_without_pair = self.removeCardsOfGivenValues(self.cards, [pair_value])

            return VALUE_PRESETS["pair"] + 100000 * pair_value + getHighestCardScore(cards_without_pair, 3)

        return 0

    def getStatistics(self, cards):
        ranks = {}
        suits = {}

        for card in cards:
            if card[0] in ranks:
                ranks[card[0]] += 1
            else:
                ranks[card[0]] = 1

            if card[1] in suits:
                suits[card[1]] += 1
            else:
                suits[card[1]] = 1

        return ranks,suits

    def getXHighestCardScore(self, values, number_of_cards_to_count):
        sorted_by_rank = sorted(values)
        return sorted_by_rank[len(values) - number_of_cards_to_count]

    def getCardWithXHighestCardScore(self, cards, number_of_cards_to_count=5):
        sorted_by_rank = sorted(cards, key=lambda x: x[0])
        return sorted_by_rank[len(cards) - number_of_cards_to_count][0]

    def getScore(self):
        funcs = [self.getStraightFlushScore, self.getFourOfKindScore, self.getFullHouseScore, self.getFlushScore,
                 self.getStraightScore, self.getThreeOfKindScore, self.getTwoPairScore, self.getPairScore]

        for func in funcs:
            score = func()
            if score != 0:
                return score

        return getHighestCardScore(self.cards, 5)