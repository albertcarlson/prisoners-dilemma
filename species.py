"""
A "list" of the different species / strategies.
"""
from utils import get_current_score, Strategy, Action, History
import random
# True = Defect
# False = Cooperate
COOP = Action.COOP
DEFECT = Action.DEFECT


class TitForTat(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP  # coop from the start
        else:
            return history.opponent_moves[-1]  # else copy opponent last moves


class ThreeChances(Strategy):
    def decide(self, history):
        if history.opponent_moves.count(DEFECT) >= 3:
            # defect forever if opponent defected 3 times in past
            return DEFECT
        else:
            return COOP


class Random(Strategy):
    def decide(self, history):
        return Action(random.getrandbits(1))
    

class Random2(Strategy):
    def decide(self, history):
        if len(history.opponent_moves) == 0:
            return COOP  # cooperate from the start
        else:
            # Select randomly from opponent's past
            # (more likely to defect if they defected a lot)
            return random.choice(history.opponent_moves)


class TitForTwoTats(Strategy):
    def decide(self, history):
        if len(history.opponent_moves) < 2:
            return COOP  # cooperate from the start
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






# ============ Species ============
    
def tit_for_tat(own: list[bool], opponent: list[bool]) -> bool:
    if len(opponent) == 0:
        return False  # cooperate from the start
    return opponent[-1]  # copy opponent last moves


def friedman_3_chances(own, opponent):
    return sum(opponent) >= 3  # defect forever if opponent defected 3 times in past


def randy(own, opponent):
    return bool(random.getrandbits(1))


def randy2(own, opponent):
    if len(opponent) == 0:
        return False  # cooperate from the start
    return random.choice(opponent)  # the more the opponent defected historically, the more likely we defect


def tit_for_two_tats(own, opponent):
    if len(opponent) < 2:
        return False  # cooperate from the start
    return opponent[-1] and opponent[-2]  # defect if they defected twice in a row


def always_defect(own, opponent):
    return True


def tester(own, opponent):
    if len(opponent) == 0:
        return True  # defect from the start
    if len(opponent) == 1:
        return False  # coop in 2nd move
    # check their response to our defect move
    if opponent[1] is False:
        # they coop even tho we started defecting
        # exploit this for the rest of the game,
        # defecting every other game
        return not len(own) % 2
    else:
        # they pushed back in 2nd move to our
        # initial defect, just play tit for tat
        return tit_for_tat(own, opponent)
    

def always_coop(own, opponent):
    return False


def resentful(own, opponent):
    # check how much we won and lost historically
    if len(opponent) == 0:
        return False  # coop from the start
    
    own_score, opponent_score = get_current_score(own, opponent)
    ahead_by = own_score - opponent_score

    if ahead_by > 5:
        # we can be nice and coop, even if 
        # they defect a little here and there
        # (FIXME: doesn't really work but whatever,
        # because as soon as they defect we are not
        # lenient since our ahead_by must go below 5
        # since we cannot be ahead by more than 9
        # with this strategy)
        return False
    elif ahead_by < -5:
        # we gotta defect on that mf some more to get ahead
        return True
    else:
        # play tit for tat
        return tit_for_tat(own, opponent)


def logician(own, opponent):
    if len(opponent) < 5:
        return randy(own, opponent)  # select a little randomly

    # if we have an average score per round >= 3,
    # keep doing what we're doing. Else do the
    # opposite
    own_score, _ = get_current_score(own, opponent)

    score_per_round = own_score / len(opponent)

    if score_per_round >= 3:
        return random.choice(own)
    else:
        return not random.choice(own)
    

def joss(own, opponent):
    if len(opponent) == 0:
        return False  # coop from the start
    
    # tit for tat, except sneaky 10% of the time
    if random.random() > 0.9:
        return True
    else:
        return tit_for_tat(own, opponent)


def selps(own, opponent):
    """
    follow the pattern
    3 coop, 1 defect, 2 coop, 5 defect
    cyclically with period 11
    """
    turn_number = len(own) + 1

    mod11 = turn_number % 11

    if mod11 in (1,2,3,5,6):
        return False  # coop
    elif mod11 in (4,7,8,9,10,0):
        return True  # defect
    assert False


def selps2(own, opponent):
    """
    follow the pattern
    4 defect, 2 coop, 6 defect, 10 coop, 4 defect, 
    2 coop, 9 defect, 19 coop, 1 defect
    cyclically with period 57
    """
    turn_number = len(own) + 1

    mod57 = turn_number % 57

    if mod57 in (5,6,13,14,15,16,17,18,19,20,21,22,27,28,38,39,40,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56):
        return False  # coop
    elif mod57 in (1,2,3,4,7,8,9,10,11,12,23,24,25,26,29,30,31,32,33,34,35,36,37,0):
        return True  # defect
    assert False


def pavlov(own, opponent):
    if len(opponent) == 0:
        return False  # coop from the start
    
    if own[-1] == opponent[-1]:
        return False  # coop if same decision
    else:
        return True  # defect if different decisions
    

def majority(own, opponent):
    if len(opponent) == 0:
        return False  # coop from the start

    return max(opponent, key=opponent.count)  # most frequent among opponent


def generous_tit_for_tat(own, opponent):
    if len(opponent) == 0:
        return False  # cooperate from the start
    
    if random.random() > 0.8:
        return False  # coop even if they defect 80% of time
    return opponent[-1]  # copy opponent last moves


def predictor(own, opponent):
    raise NotImplementedError("Not made yet")
    predicted_opponent_move = ...

    return predicted_opponent_move  # copy what we predict they'll do


def angry_revenge(own, opponent):
    return sum(opponent) > 0  # defect forever if opponent defected once





SPECIES = [
    tit_for_tat,
    friedman_3_chances,
    randy,
    randy2,
    tit_for_two_tats,
    always_defect,
    tester,
    always_coop,
    resentful,
    logician,
    joss,
    selps,
    selps2,
    pavlov,
    majority,
    generous_tit_for_tat,
    angry_revenge,
]

