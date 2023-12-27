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


class Action(Enum):
    COOP: bool = False
    DEFECT: bool = True

    def __invert__(self):
        return Action(not self.value)


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


class Strategy(ABC):
    @abstractmethod
    def decide(self, history: History) -> Action:
        pass


class Player:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        self.score = 0

    def make_decision(self, history):
        return self.strategy.decide(history)
    
    def __repr__(self):
        return f"<Player object at {hex(id(self))} using {self.strategy.__class__.__name__} strategy with score={self.score}>"
    