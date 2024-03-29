'''
Where we test the hand evaluator.
'''

from evaluator import *

def testStraightFlush():
    straight_flush_preset = VALUE_PRESETS["straight_flush"]

    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]) == straight_flush_preset + 4)
    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 1]]) == straight_flush_preset + 3)
    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 1], [8, 1]]) == straight_flush_preset + 2)
    assert (getHandScore([[6, 0], [3, 0], [4, 0], [5, 0], [7, 0], [7, 1], [8, 1]]) == straight_flush_preset + 3)
    hand = [[2, 0], [3, 0], [4, 0], [5, 0], [11, 1], [7, 1], [8, 1]]
    assert (getHandScore(hand) == getHighestCardScore(hand, 5))
    hand = [[6, 0], [3, 0], [4, 0], [5, 0], [11, 1], [9, 1], [1, 1]]
    hand_with_aces = [[6, 0], [3, 0], [4, 0], [5, 0], [11, 1], [9, 1], [14, 1]]
    assert (getHandScore(hand) == getHighestCardScore(hand_with_aces, 5))
    assert (getHandScore([[2, 0], [3, 0], [4, 0], [5, 0], [6, 1], [7, 1], [1, 0]]) == straight_flush_preset + 1)
    assert (getHandScore([[12, 0], [11, 0], [10, 0], [13, 0], [6, 1], [7, 1], [1, 0]]) == straight_flush_preset + 10)

def testFourOfAKind():
    four_of_a_kind_preset = VALUE_PRESETS["four_of_kind"]

    assert (getHandScore([[2, 0], [2, 1], [2, 2], [2, 3], [11, 0], [7, 1], [8, 0]]) == four_of_a_kind_preset + 11)
    assert (getHandScore([[12, 0], [12, 1], [12, 2], [12, 3], [11, 0], [7, 1], [8, 0]]) == four_of_a_kind_preset + 11)
    assert (getHandScore([[12, 0], [12, 1], [12, 2], [12, 3], [1, 0], [7, 1], [8, 0]]) == four_of_a_kind_preset + 14)
    assert (getHandScore([[12, 0], [12, 1], [12, 2], [12, 3], [2, 0], [7, 1], [8, 0]]) == four_of_a_kind_preset + 8)
    hand = [[2, 0], [3, 0], [4, 2], [5, 2], [11, 0], [7, 1], [8, 0]]
    assert (getHandScore(hand) == getHighestCardScore(hand, 5))

def testFullHouse():
    full_house_preset = VALUE_PRESETS["full_house"]

    assert (getHandScore([[12, 0], [12, 1], [12, 2], [7, 3], [2, 0], [7, 1], [8, 0]]) == full_house_preset + 240 + 7)
    assert (getHandScore([[2, 0], [2, 1], [12, 2], [7, 3], [2, 0], [7, 1], [8, 0]]) == full_house_preset + 40 + 7)
    assert (getHandScore([[2, 0], [2, 1], [12, 2], [7, 3], [2, 0], [12, 1], [8, 0]]) == full_house_preset + 40 + 12)
    assert (getHandScore([[2, 0], [2, 1], [12, 2], [7, 3], [2, 0], [12, 1], [7, 0]]) == full_house_preset + 40 + 12)
    assert (getHandScore([[2, 0], [2, 1], [3, 2], [7, 3], [2, 0], [3, 1], [7, 0]]) == full_house_preset + 40 + 7)

def testFlush():
    flush_preset = VALUE_PRESETS["flush"]

    assert (getHandScore([[12, 0], [12, 1], [11, 0], [7, 3], [2, 0], [7, 0], [8, 0]]) == flush_preset + 40)
    assert (getHandScore([[12, 0], [12, 1], [11, 0], [7, 3], [1, 0], [7, 0], [8, 0]]) == flush_preset + 52)
    assert (getHandScore([[1, 0], [10, 0], [3, 0], [8, 0], [4, 0], [5, 0], [6, 0]]) == flush_preset + 43)
    assert (getHandScore([[1, 0], [10, 0], [3, 0], [8, 0], [4, 0], [5, 0], [7, 0]]) == flush_preset + 44)

def testStraight():
    straight_preset = VALUE_PRESETS["straight"]

    assert (getHandScore([[12, 0], [12, 1], [11, 0], [10, 3], [9, 0], [8, 1], [7, 3]]) == straight_preset + 8)
    assert (getHandScore([[13, 0], [1, 1], [11, 0], [10, 3], [9, 0], [8, 1], [7, 3]]) == straight_preset + 7)
    assert (getHandScore([[2, 0], [1, 1], [3, 0], [4, 3], [5, 0], [8, 1], [7, 3]]) == straight_preset + 1)

def testThreeOfAKind():
    three_kind_preset = VALUE_PRESETS["three_of_kind"]

    assert (getHandScore([[12, 0], [12, 1], [12, 0], [10, 3], [9, 0], [8, 1], [7, 3]]) ==
            three_kind_preset + 10000 * 12 + 20 * 10 + 9)
    assert (getHandScore([[2, 0], [2, 1], [2, 0], [10, 3], [9, 0], [8, 1], [7, 3]]) ==
            three_kind_preset + 10000 * 2 + 20 * 10 + 9)
    assert (getHandScore([[6, 0], [6, 1], [6, 0], [1, 3], [13, 0], [8, 1], [7, 3]]) ==
            three_kind_preset + 10000 * 6 + 20 * 14 + 13)

def testTwoPair():
    two_pair_preset = VALUE_PRESETS["two_pair"]

    assert (getHandScore([[12, 0], [12, 1], [10, 0], [10, 3], [9, 0], [8, 1], [7, 3]]) == two_pair_preset + 2400 + 100 + 9)
    assert (getHandScore([[12, 0], [12, 1], [10, 0], [10, 3], [8, 0], [8, 1], [7, 3]]) == two_pair_preset + 2400 + 100 + 8)
    assert (getHandScore([[12, 0], [12, 1], [10, 0], [10, 3], [1, 0], [1, 1], [7, 3]]) == two_pair_preset + 2800 + 120 + 10)
    assert (getHandScore([[2, 0], [2, 1], [3, 0], [6, 3], [1, 0], [1, 1], [4, 3]]) == two_pair_preset + 2800 + 20 + 6)
    assert (getHandScore([[12, 0], [12, 1], [8, 0], [1, 3], [13, 0], [13, 1], [7, 3]]) == two_pair_preset + 2600 + 120 + 14)

def testPair():
    pair_preset = VALUE_PRESETS["pair"]

    assert (getHandScore([[13, 0], [13, 1], [10, 0], [5, 3], [9, 0], [8, 1], [7, 3]]) ==
            pair_preset + 100000 * 13 + 400 * 10 + 20 * 9 + 8)
    assert (getHandScore([[12, 0], [12, 1], [10, 0], [5, 3], [9, 0], [8, 1], [7, 3]]) ==
            pair_preset + 100000 * 12 + 400 * 10 + 20 * 9 + 8)
    assert (getHandScore([[1, 0], [1, 1], [10, 0], [5, 3], [9, 0], [4, 1], [7, 3]]) ==
            pair_preset + 100000 * 14 + 400 * 10 + 20 * 9 + 7)

def testHighCard():
    assert (getHandScore([[13, 0], [1, 1], [10, 0], [5, 3], [9, 0], [8, 1], [7, 3]]) ==
            160000 * 14 + 8000 * 13 + 400 * 10 + 20 * 9 + 8)
    assert (getHandScore([[13, 0], [1, 1], [10, 0], [11, 3], [9, 0], [8, 1], [6, 3]]) ==
            160000 * 14 + 8000 * 13 + 400 * 11 + 20 * 10 + 9)
    assert (getHandScore([[13, 0], [1, 1], [12, 0], [11, 3], [2, 0], [3, 1], [4, 3]]) ==
            160000 * 14 + 8000 * 13 + 400 * 12 + 20 * 11 + 4)
    assert (getHandScore([[13, 0], [1, 1], [12, 0], [6, 3], [2, 0], [3, 1], [4, 3]]) ==
            160000 * 14 + 8000 * 13 + 400 * 12 + 20 * 6 + 4)
    assert (getHandScore([[13, 0], [1, 1], [11, 0], [10, 3], [2, 0], [3, 1], [9, 3]]) ==
            160000 * 14 + 8000 * 13 + 400 * 11 + 20 * 10 + 9)

def testHands():
    testStraightFlush()
    testFourOfAKind()
    testFullHouse()
    testFlush()
    testStraight()
    testThreeOfAKind()
    testTwoPair()
    testPair()
    testHighCard()