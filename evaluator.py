VALUE_PRESETS = {"straight_flush" : 10000, "four_of_kind" : 9000, }

class HandEvaluator(object):
    def __init__(self, cards):
        if len(cards) == 7:
            self.cards = cards
            self.sorted_by_rank = sorted(cards, key=lambda x: x[0])
            self.sorted_by_suit = sorted(cards, key=lambda x: x[1])
        else:
            raise Exception("no point calculating score without all cards on table")

    def getStraightFlushScore(self, cards):
        return 0

    def getFourOfKindScore(self, cards):
        return 0

    def getFullHouseScore(self, cards):
        return 0

    def getFlushScore(self, cards):
        return 0

    def getStraightScore(self, cards):
        return 0

    def getThreeOfKindScore(self, cards):
        return 0

    def getTwoPairScore(self, cards):
        return 0

    def getTopPairScore(self, cards):
        return 0

    def getHighCardScore(self, cards, number_of_cards_to_count=5):
        return self.sorted_by_rank[len(cards) - number_of_cards_to_count][0]

    def getScore(self):
        funcs = [self.getStraightFlushScore, self.getFourOfKindScore, self.getFullHouseScore, self.getFlushScore,
                 self.getStraightScore, self.getThreeOfKindScore, self.getTwoPairScore, self.getTopPairScore,
                 self.getHighCardScore]

        for func in funcs:
            score = func(self.cards)
            if score != 0:
                return score

        return -1