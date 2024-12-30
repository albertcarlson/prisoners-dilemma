"""
A "list" of the different species / strategies.
"""
from utils import Strategy, Action, History, random_action
import random


# Make the Action enum values more accessible
COOP = Action.COOP
DEFECT = Action.DEFECT



# ============ Species ============


class TitForTat(Strategy):
    """
    Starts by cooperating, then does whatever the opponent did last
    """
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        else:
            return history.opponent_moves[-1]


class ThreeChances(Strategy):
    """
    Defects forever if opponent defected 3 or more times in past,
    otherwise cooperates
    """
    def decide(self, history):
        if history.opponent_moves.count(DEFECT) >= 3:
            # defect forever if opponent defected 3 times in past
            return DEFECT
        else:
            return COOP


class Random(Strategy):
    """
    Randomly selects an action with equal probability each turn
    """
    def decide(self, history):
        return random_action()
    

class Random2(Strategy):
    """
    Randomly selects an action with probability based on opponent's past.
    E.g. in the 11th turn, if the opponent defected 8 times and cooperated
    2 times in the first 10 turns, the probability of defecting is 8/10 = 80%
    """
    def decide(self, history):
        if len(history.opponent_moves) == 0:
            return COOP
        else:
            # Select randomly from opponent's past
            # (more likely to defect if they defected a lot)
            return random.choice(history.opponent_moves)


class TitForTwoTats(Strategy):
    """
    Starts by cooperating, then defects if opponent defects twice in a row
    """
    def decide(self, history):
        if len(history.opponent_moves) < 2:
            return COOP
        elif history.opponent_moves[-1] == DEFECT and history.opponent_moves[-2] == DEFECT:
            return DEFECT  # defect if they defected twice in a row
        else:
            return COOP


class AlwaysDefect(Strategy):
    """
    Always defects, regardless of opponent's actions
    """
    def decide(self, history):
        return DEFECT
    

class AlwaysCoop(Strategy):
    """
    Always cooperates, regardless of opponent's actions
    """
    def decide(self, history):
        return COOP


class Tester(Strategy):
    """
    Tries to exploit generous strategies:
    - Defects in first move
    - Cooperates in second and third move, and checks opponent's response
    - Keeps exploiting every other move if opponent cooperates in 2nd move,
    - Otherwise plays Tit for Tat
    """
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return DEFECT  # defect from the start
        elif len(history) in (1, 2):
            return COOP  # coop in 2nd and 3rd move
        
        # check their response to our initial defect
        elif history.opponent_moves[1] == COOP:
            # they coop in 2nd even tho we defected in first
            # exploit this for the rest of the game, defect every other game
            return Action(len(history) % 2)
        else:
            # they pushed back in 2nd move to our
            # initial defect, just play tit for tat
            return history.opponent_moves[-1] 


class Joss(Strategy):
    """
    Tit for Tat, except with 10% probability it may
    defect for no reason, trying to be sneaky
    """
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP  # coop from the start
    
        # tit for tat, except sneaky 10% of the time
        if random.random() > 0.9:
            return DEFECT
        else:
            return history.opponent_moves[-1]


class Pavlov(Strategy):
    """
    Starts by cooperating, then coops if it did the same as the
    opponent last move, otherwise defects if they did different moves.
    """
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        
        if history.own_moves[-1] == history.opponent_moves[-1]:
            return COOP  # coop if same decision last
        else:
            return DEFECT  # defect if different decisions


class Majority(Strategy):
    """
    Starts by cooperating, then does what the opponent most frequently
    did in the past.
    """
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP

        # most frequent among opponent 
        return max(history.opponent_moves, key=history.opponent_moves.count)


class GenerousTitForTat(Strategy):
    """
    Tit for Tat, except might coop occasionally (20% chance)
    despite the opponent defecting.
    
    Tries to escape "viscious cycles of defection" against
    other otherwise nice strategies this way
    """
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
    
        if random.random() > 0.8:
            return COOP  # coop even if they defect, 80% of the time
        return history.opponent_moves[-1]


class AngryRevenge(Strategy):
    """
    Coops until the opponent defects once, then always defects
    """
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP

        if history.opponent_moves.count(DEFECT) > 0:
            # defect forever if opponent defected once
            return DEFECT
        else:
            return COOP



EXAMPLE_SPECIES: dict[str, Strategy] = {
    strat.__class__.__name__: strat
    for strat in [
        TitForTat(),
        ThreeChances(),
        Random(),
        Random2(),
        TitForTwoTats(),
        AlwaysDefect(),
        AlwaysCoop(),
        Tester(),
        Joss(),
        Pavlov(),
        Majority(),
        GenerousTitForTat(),
        AngryRevenge(),
    ]
}
