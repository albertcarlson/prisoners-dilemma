"""
These were the 19 strategies submitted on Farum Camp when
asking for strategies to compete in the simulation. Note
that I mentioned that each battle lasts for 10 rounds, so
some submissions rely on this constant. Therefore, you
should only play with these with the rounds set to 10.
"""
from utils import Strategy, Action, History, random_action
import random


# Make the Action enum values more accessible
COOP = Action.COOP
DEFECT = Action.DEFECT



class CaveMom(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) in (4, 7, 9):
            return DEFECT
        return COOP
    
class Noah(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        if len(history) >= 7:
            return DEFECT
        num_defects = history.opponent_moves.count(DEFECT)
        p = (num_defects+2) / (len(history)+2)
        if random.random() < p:
            return DEFECT
        return COOP

class GreedIsGood(Strategy):
    def decide(self, history: History) -> Action:
        return DEFECT

class TheGrudgeholder(Strategy):
    def decide(self, history: History) -> Action:
        if history.opponent_moves.count(DEFECT) >= 2:
            return DEFECT
        else:
            return COOP

class Louise(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) < 5:
            return COOP
        return DEFECT
    
class NanaChrissyboy(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        return DEFECT

class Larqurion(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) > 2 and history.opponent_moves[-1] == DEFECT and history.opponent_moves[-2] == DEFECT:
            return DEFECT
        if random.random() < 1/3:
            return DEFECT
        return COOP
    
class TheBook(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        if len(history) == 9:
            return DEFECT
        if random.random() < 0.1:
            return COOP
        return history.opponent_moves[-1]
    
class DiaDeLosMuertos(Strategy):
    def decide(self, history: History) -> Action:
        turn_number = len(history) + 1
        if random.random() < turn_number / 10:
            return DEFECT
        return COOP

class Random(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) in (4, 5, 6, 8):
            return COOP
        return DEFECT
    
class NinePctFruktsaft(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        if len(history) >= 7:
            return DEFECT
        return history.opponent_moves[-1]

class ThePsychopath(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) <= 1:
            return COOP
        if len(history) == 9:
            return DEFECT
        if history.opponent_moves[-1] == DEFECT and history.opponent_moves[-2] == DEFECT:
            return DEFECT
        return COOP
    
class TrunkatedTFT(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        if len(history) >= 7:
            return DEFECT
        return history.opponent_moves[-1]
    
class Slowpoke(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) <= 1:
            return COOP
        if history.opponent_moves[-2] == DEFECT:
            return DEFECT
        return COOP
        
class Manslaughter(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return DEFECT
        if history.opponent_moves[-1] == DEFECT:
            return COOP
        return DEFECT

class Linnestad(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        if len(history) >= 7:
            return DEFECT
        if history.opponent_moves[-1] == DEFECT:
            return DEFECT
        return COOP

class SpaghettiMedSmør(Strategy):
    def decide(self, history: History) -> Action:
        nth_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29][len(history)]
        nth_fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55][len(history)]
        if ((nth_prime**2) % nth_fibonacci) % 2:
            return DEFECT
        return COOP

class TheSneakySnake(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) in (0, 9):
            return DEFECT
        
        tf2t = "1101010101"

        if history.opponent_moves[0] == DEFECT:
            # play tit for tat
            return history.opponent_moves[-1]
        else:
            if tf2t[9-len(history)] == "1":
                return DEFECT
            return COOP

class Tomas(Strategy):
    def decide(self, history: History) -> Action:
        if len(history) == 0:
            return COOP
        if len(history) == 9:
            return DEFECT
        if history.opponent_moves[-1] == DEFECT:
            return DEFECT
        return COOP
        



FARUM_CAMP_SPECIES: dict[str, Strategy] = {
    strat.__class__.__name__: strat
    for strat in [
        CaveMom(),
        Noah(),
        GreedIsGood(),
        TheGrudgeholder(),
        Louise(),
        NanaChrissyboy(),
        Larqurion(),
        TheBook(),
        DiaDeLosMuertos(),
        Random(),
        NinePctFruktsaft(),
        ThePsychopath(),
        TrunkatedTFT(),
        Slowpoke(),
        Manslaughter(),
        Linnestad(),
        SpaghettiMedSmør(),
        TheSneakySnake(),
        Tomas()
    ]
}
