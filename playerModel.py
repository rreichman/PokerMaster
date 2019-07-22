'''
ML model of the poker player
'''

import tensorflow as tf

class Action(object):
    # Type is Raise;Call;Fold and value is how much (only relevant for Raises)
    def __init__(self, type, value):
        self.type = type
        self.value = value

class PlayerModel(object):
    def __init__(self):
        pass

    # NOTE - Currently we keep other player's cards in the state. Make sure that you're not looking at other player's
    # cards (using them in the model)!
    def act(self, state):
        return Action("Raise", 100)