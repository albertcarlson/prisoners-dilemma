"""
A "list" of the different species / strategies.
"""
from tools import get_score_from_history, Strategy, Action, History, random_action
import random

from tools.tools import Action, History

# Make the Action enum values more accessible
COOP = Action.COOP
DEFECT = Action.DEFECT



# ============ Species ============


class TitForTat(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        else:
            return history.opponent_moves[-1]


class ThreeChances(Strategy):
    def decide(self, history):
        if history.opponent_moves.count(DEFECT) >= 3:
            # defect forever if opponent defected 3 times in past
            return DEFECT
        else:
            return COOP


class Random(Strategy):
    def decide(self, history):
        return random_action()
    

class Random2(Strategy):
    def decide(self, history):
        if len(history.opponent_moves) == 0:
            return COOP
        else:
            # Select randomly from opponent's past
            # (more likely to defect if they defected a lot)
            return random.choice(history.opponent_moves)


class TitForTwoTats(Strategy):
    def decide(self, history):
        if len(history.opponent_moves) < 2:
            return COOP
        elif history.opponent_moves[-1] == DEFECT and history.opponent_moves[-2] == DEFECT:
            return DEFECT  # defect if they defected twice in a row
        else:
            COOP


class AlwaysDefect(Strategy):
    def decide(self, history):
        return DEFECT
    

class AlwaysCoop(Strategy):
    def decide(self, history):
        return COOP


class Tester(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return DEFECT  # defect from the start
        elif len(history) == 1:
            return COOP  # coop in 2nd move
        
        # check their response to our initial defect
        elif history.opponent_moves[1] == COOP:
            # they coop in 2nd even tho we defected in first
            # exploit this for the rest of the game, defect every other game
            return Action(not len(history) % 2)
        else:
            # they pushed back in 2nd move to our
            # initial defect, just play tit for tat
            return history.opponent_moves[-1] 


class RepeatWhatWorks(Strategy):
    def decide(self, history):
        if len(history) < 5:
            # start off randomly
            return random_action()

        own_score, opponent_score = get_score_from_history(history)
        
        if own_score >= opponent_score:
            # if ahead, keep doing what we're doing
            return random.choice(history.own_moves)
        
        else:
            # do the "opposite" of a random choice
            return ~random.choice(history.own_moves)


class Joss(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP  # coop from the start
    
        # tit for tat, except sneaky 10% of the time
        if random.random() > 0.9:
            return DEFECT
        else:
            return history.opponent_moves[-1]


class Selps(Strategy):
    """
    follow the pattern
    3 coop, 1 defect, 2 coop, 5 defect
    cyclically with period 11
    """
    def decide(self, history: History) -> Action:
        turn_number = len(history) + 1
        mod11 = turn_number % 11
        if mod11 in (1, 2, 3, 5, 6):
            return COOP
        elif mod11 in (4, 7, 8, 9, 10, 0):
            return DEFECT
        assert False


class Pavlov(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        
        if history.own_moves[-1] == history.opponent_moves[-1]:
            return COOP  # coop if same decision last
        else:
            return DEFECT  # defect if different decisions


class Majority(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP

        # most frequent among opponent 
        return max(history.opponent_moves, key=history.opponent_moves.count)


class GenerousTitForTat(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
    
        if random.random() > 0.8:
            return COOP  # coop even if they defect, 80% of the time
        return history.opponent_moves[-1]


class AngryRevenge(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP

        if history.opponent_moves.count(DEFECT) > 0:
            # defect forever if opponent defected once
            return DEFECT
        else:
            return COOP



SPECIES = [
    TitForTat,
    ThreeChances,
    Random,
    Random2,
    TitForTwoTats,
    AlwaysDefect,
    AlwaysCoop,
    Tester,
    RepeatWhatWorks,
    Joss,
    Selps,
    Pavlov,
    Majority,
    GenerousTitForTat,
    AngryRevenge,
]
