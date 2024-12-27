"""
This file contains important, yet semi-ugly
/ abstract datatypes that are used throughout
the project. It is intended to only be imported
by other files in the project to ensure a clean
API.
"""

from collections.abc import MutableSequence
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
import configparser



class Action(Enum):
    COOP: bool = False
    DEFECT: bool = True

    def __invert__(self):
        return Action(not self.value)



def _read_payoff_matrix(filename="config.ini") -> dict[tuple[Action, Action], tuple[int, int]]:
    """Reads the payoff matrix from the config file.
    Returns a dictionary of (Action, Action) -> (int, int) mappings."""    
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        (Action.COOP, Action.COOP): tuple(map(int, config.get('PayoffMatrix', 'CoopCoop').split(','))),
        (Action.COOP, Action.DEFECT): tuple(map(int, config.get('PayoffMatrix', 'CoopDefect').split(','))),
        (Action.DEFECT, Action.COOP): tuple(map(int, config.get('PayoffMatrix', 'DefectCoop').split(','))),
        (Action.DEFECT, Action.DEFECT): tuple(map(int, config.get('PayoffMatrix', 'DefectDefect').split(','))),
    }

PAYOFF_MATRIX = _read_payoff_matrix()



@dataclass
class History:
    own_moves: MutableSequence[Action] = field(default_factory=list)  # Weird due to mutability
    opponent_moves: MutableSequence[Action] = field(default_factory=list)
    
    def append(self, own_move: Action, opponent_move: Action) -> None:
        self.own_moves.append(own_move)
        self.opponent_moves.append(opponent_move)
    
    def __len__(self):
        return len(self.own_moves)

    def __iter__(self):
        return zip(self.own_moves, self.opponent_moves)
    
    def __invert__(self):
        """Returns a new History object with the moves swapped,
        so that the opponent's moves are now our moves and vice versa."""
        return History(self.opponent_moves, self.own_moves)
    
    @property
    def score(self) -> tuple[int, int]:
        """Returns a tuple of (own_score, opponent_score) from a History object."""
        own_score = 0
        opponent_score = 0
        for own_move, opponent_move in self:
            
            own_increase, opponent_increase = PAYOFF_MATRIX[own_move, opponent_move]
            own_score += own_increase
            opponent_score += opponent_increase

        return own_score, opponent_score

    def __repr__(self) -> str:
        return f"History(own_moves={self.own_moves}, opponent_moves={self.opponent_moves})"

    def __str__(self) -> str:
        """
        Prints a nice representation of a History object.
        
        Example:
        >>> history = History(
        ...     own_moves=[COOP, COOP, DEFECT, COOP, DEFECT, COOP],
        ...     opponent_moves=[DEFECT, DEFECT, DEFECT, COOP, COOP, DEFECT]
        ... )
        H ··×·×·
        A ×××··×
        # (with colors, that can't be shown here)    
        """
        coop_letter = "·"
        defect_letter = "×"
        def handle_line(lst):
            return "".join(f"\x1b[32m{coop_letter}\x1b[0m" if elem == Action.COOP else f"\x1b[31m{defect_letter}\x1b[0m" for elem in lst)
        
        return "H " + handle_line(self.own_moves) + "\n" + "A " + handle_line(self.opponent_moves)



class Strategy(ABC):
    @abstractmethod
    def decide(self, history: History) -> Action:
        pass



class Player:
    def __init__(self, strategy: Strategy):
        self.strategy_name = strategy.__class__.__name__
        self.strategy = strategy
        # self.score = 0  #NotImplemented

    def make_decision(self, history):
        return self.strategy.decide(history)
        
    def __repr__(self):
        return f"<Player object at {hex(id(self))} using {self.strategy_name}>"


