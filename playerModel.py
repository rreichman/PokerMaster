'''
ML model of the poker player
'''

import random
import tensorflow as tf

class Action(object):
    # Type is Raise;Call;Fold and value is how much (only relevant for Raises)
    def __init__(self, type, value = 0):
        self.type = type
        self.value = value

actions = [Action("Raise", 100), Action("Check"), Action("Fold")]

class PlayerModel(object):
    def __init__(self):
        pass

    # NOTE - Currently we keep other player's cards in the state. Make sure that you're not looking at other player's
    # cards (using them in the model)!
    def act(self, state):
        # Start with a random policy that just goes all-in, calls, or folds arbitrarily. Once the workflow is good for
        # that we can move to more interesting policies.
        action_index = random.randint(0,len(actions) - 1)
        return actions[action_index]