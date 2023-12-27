"""
Library for various helper tools.
E.g. getting the curent scores,
printing moves in a nice way,
adjusting populations, etc.
"""
# _PAYOFF_MATRIX = {
#     (True, True): (1, 1),
#     (True, False): (5, 0),
#     (False, True): (0, 5),
#     (False, False): (3, 3)  
# }  #Idea to implement: assymetric rewards. This might model real life better.
#    #maybe something like an "alpha/bully" and a "weakling" where the weakling
#    #might risk getting -1 for defecting or something idk
# from dict_zip import dict_zip
# from typing import Callable
# import json




# def get_current_score(own: list[bool], opponent: list[bool]) -> tuple[int, int]:
#     own_score = 0
#     opponent_score = 0
#     for own_move, opponent_move in zip(own, opponent):
        
#         own_increase, opponent_increase = _PAYOFF_MATRIX[(own_move, opponent_move)]
#         own_score += own_increase
#         opponent_score += opponent_increase

#     return own_score, opponent_score


# def battle(
#     species1: Callable[[list[bool], list[bool]], bool],
#     species2: Callable[[list[bool], list[bool]], bool],
#     *,
#     rounds: int = 100,
#     verbose: bool = False,
# ) -> tuple[int, int]:
    
#     species1_moves = []
#     species2_moves = []

#     for _ in range(rounds):
#         species1_move = species1(species1_moves, species2_moves)
#         species2_move = species2(species2_moves, species1_moves)
#         assert species1_move in [True, False], f"WHAT, it made this move: {species1_move}. (Species={species1.__name__})"
#         assert species2_move in [True, False], f"WHAT, it made this move: {species2_move}. (Species={species2.__name__})"

#         species1_moves.append(species1_move)
#         species2_moves.append(species2_move)

#     assert len(species1_moves) == len(species2_moves) == rounds
#     if verbose:
#         print_moves(species1_moves)
#         print_moves(species2_moves)
#     return get_current_score(species1_moves, species2_moves)


# def print_moves(defect_coop: list[bool]) -> None:
#     print("".join("\x1b[32m.\x1b[0m" if elem is False else "\x1b[31mx\x1b[0m" for elem in defect_coop))


# def adjust_populations(populations: dict, avg_scores_per_round: dict) -> dict:
#     """
#     Given a dictionary of (species: population before generation) mappings
#     and a dictionary of (species: avg. score per round in the generation) 
#     mappings, adjust the populations accordingly.
    
#     populations.keys() must be equal to avg_scores_per_round.keys().
#     """
#     if populations.keys() != avg_scores_per_round.keys():
#         raise ValueError("populations.keys() must be equal to avg_scores_per_round.keys().")

#     weighted_average_score = sum(
#         population * avg_score
#         for species, (population, avg_score) in dict_zip(populations, avg_scores_per_round).items()
#     ) / sum(populations.values())
    
#     # find out which are above and below the average, to figure out which
#     # populations to increase and decrease
#     above_average = {
#         species: avg_score
#         for species, avg_score in avg_scores_per_round.items()
#         if avg_score > weighted_average_score
#     }
#     below_average = {
#         species: avg_score
#         for species, avg_score in avg_scores_per_round.items()
#         if avg_score < weighted_average_score
#     }

#     # Adjust populations
#     for species in above_average:
#         # FIXME L8R: maybe increase by a percentage instead of 1? 
#         # So if much ahead, grow more in population than if just a little ahead?
#         populations[species] += 1  

#     for species in below_average:
#         populations[species] -= 1

#     return populations


# def save_scores_2_json(avg_scores_per_round: dict, filename: str = "results.json") -> None:
#     sorted_scores = dict(sorted(avg_scores_per_round.items(), key=lambda x: x[1], reverse=True))
    
#     if callable(list(sorted_scores.keys())[0]):
#         sorted_scores = {
#             species.__name__: score
#             for species, score in sorted_scores.items()
#         }

#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(sorted_scores, f, indent=4, ensure_ascii=False)


# def summary(avg_scores_per_round: dict) -> str:
#     """
#     Given the average scores for each, write a quick summary
    
#     >>> summary({
#     ...     "Tit for tat": 250,
#     ...     "Defector": 220,
#     ...     "Josh": 215,
#     ... })
#     "The 1st place is Tit for tat with avg. score of 250, while the worst is Josh, who only got 215. The average score was 22.8 among 3 participants."
#     """
#     sorted_scores = sorted(avg_scores_per_round.items(), key=lambda x: x[1], reverse=True)
#     best = sorted_scores[0]
#     worst = sorted_scores[-1]
#     avg_score = sum(avg_scores_per_round.values()) / len(avg_scores_per_round)
#     total_participants = len(avg_scores_per_round)

#     # if the keys are function objects
#     if callable(best[0]):
#         best  = (best[0].__name__,  best[1])
#         worst = (worst[0].__name__, worst[1])
        

#     return f"The 1st place is {best[0]} with avg. score of {best[1]}, while the worst is {worst[0]}, who only got {worst[1]}. The average score was {avg_score:.1f} among {total_participants} participants."




from collections.abc import MutableSequence
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
import random


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
        return f"<Player using {self.strategy.__class__.__name__} strategy>"
    

def random_action() -> Action:
    """Simple utility function to avoid
    having to type Action(random.getrandbits(1))."""
    return Action(random.getrandbits(1))



__PAYOFF_MATRIX = {
    (Action.COOP, Action.COOP): (3, 3),
    (Action.COOP, Action.DEFECT): (0, 5),
    (Action.DEFECT, Action.COOP): (5, 0),
    (Action.DEFECT, Action.DEFECT): (1, 1)  
}  #Idea to implement: assymetric rewards. This might model real life better.
   #maybe something like an "alpha/bully" and a "weakling" where the weakling
   #might risk getting -1 for defecting or something idk


def get_score_from_history(history: History) -> tuple[int, int]:
    """Returns a tuple of (own_score, opponent_score) from a History object."""
    own_score = 0
    opponent_score = 0
    for own_move, opponent_move in history:
        
        own_increase, opponent_increase = __PAYOFF_MATRIX[(own_move, opponent_move)]
        own_score += own_increase
        opponent_score += opponent_increase

    return own_score, opponent_score