VALUE_PRESETS = {"straight_flush" : 10000, "four_of_kind" : 9000, "full_house" : 8000, "flush" : 7000,
                 "straight": 6000, "three_of_kind" : 5000, "two_pair" : 4000, "pair" : 3000, "high_card" : 2000}

class HandEvaluator(object):
    def __init__(self, cards):
        if len(cards) == 7:
            self.cards = cards
            self.ranks_count, self.suits_count = self.getStatistics(self.cards)
            self.inv_ranks_count = {v: k for k, v in self.ranks_count.items()}
            self.sorted_flush_cards = sorted(self.getFlushCardsIfExists(), key=lambda x: x[0])
        else:
            raise Exception("no point calculating score without all cards on table")

    def getStraightFlushScore(self):
        if len(self.sorted_flush_cards) > 0:
            longest_streak = [self.sorted_flush_cards[0]]

            for i in range(len(self.sorted_flush_cards) - 1):
                if self.sorted_flush_cards[i][0] == self.sorted_flush_cards[i + 1][0] - 1:
                    longest_streak.append(self.sorted_flush_cards[i + 1])
                else:
                    if len(longest_streak) >= 5:
                        break
                    if len(longest_streak) > len(self.sorted_flush_cards) - i:
                        break
                    longest_streak = [self.sorted_flush_cards[i+1]]

            if len(longest_streak) >= 5:
                return VALUE_PRESETS["straight_flush"] + self.getHighCardScore(longest_streak)

        return 0

    def getFourOfKindScore(self):
        if 4 in self.ranks_count.values():
            four_of_kind_value = self.inv_ranks_count[4]

            cards_without_four_of_kind = []
            for card in self.cards:
                if card[0] != four_of_kind_value:
                    cards_without_four_of_kind.append(card)

            return VALUE_PRESETS["four_of_kind"] + \
                   self.getHighCardScore(cards_without_four_of_kind, number_of_cards_to_count=1)

        return 0

    def getFullHouseScore(self):
        if 3 in self.ranks_count.values() and 2 in self.ranks_count.values():
            rank_appearing_three_times = self.inv_ranks_count[3]
            highest_two_card = 0
            for rank in self.ranks_count:
                rank_appearances = self.ranks_count[rank]
                if rank_appearances == 2 and rank > highest_two_card:
                    highest_two_card = rank

            return VALUE_PRESETS["full_house"] + 10 * rank_appearing_three_times + highest_two_card

        return 0

    def getFlushCardsIfExists(self):
        for suit in self.suits_count:
            if self.suits_count[suit] >= 5:
                flush_cards = []
                for card in self.cards:
                    if card[1] == suit:
                        flush_cards.append(card)
                return flush_cards

        return []

    def getFlushScore(self):
        if len(self.sorted_flush_cards) >= 5:
            val = 0
            for i in range(5):
                val += self.sorted_flush_cards[len(self.sorted_flush_cards) - 5 + i][0]
            return VALUE_PRESETS["flush"] + val

        return 0

    def getStraightScore(self):
        return 0

    def getThreeOfKindScore(self):
        return 0

    def getTwoPairScore(self):
        return 0

    def getPairScore(self):
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

    def getHighCardScore(self, cards, number_of_cards_to_count=5):
        sorted_by_rank = sorted(cards, key=lambda x: x[0])
        return sorted_by_rank[len(cards) - number_of_cards_to_count][0]

    def getScore(self):
        funcs = [self.getStraightFlushScore, self.getFourOfKindScore, self.getFullHouseScore, self.getFlushScore,
                 self.getStraightScore, self.getThreeOfKindScore, self.getTwoPairScore, self.getPairScore]

        for func in funcs:
            score = func()
            if score != 0:
                return score

        return self.getHighCardScore(self.cards)