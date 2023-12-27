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

from utils.dtypes import Action, History
import random


def random_action() -> Action:
    """Simple utility function to avoid
    having to type Action(random.getrandbits(1))."""
    return Action(random.getrandbits(1))



__PAYOFF_MATRIX = {
    (Action.COOP, Action.COOP): (3, 3),
    (Action.COOP, Action.DEFECT): (0, 5),
    (Action.DEFECT, Action.COOP): (5, 0),
    (Action.DEFECT, Action.DEFECT): (1, 1)  
}  # Idea to implement: assymetric rewards. This might model real life better.
   # maybe something like an "alpha/bully" and a "weakling" where the weakling
   # might risk getting -1 for defecting or something idk


def get_score_from_history(history: History) -> tuple[int, int]:
    """Returns a tuple of (own_score, opponent_score) from a History object."""
    own_score = 0
    opponent_score = 0
    for own_move, opponent_move in history:
        
        own_increase, opponent_increase = __PAYOFF_MATRIX[own_move, opponent_move]
        own_score += own_increase
        opponent_score += opponent_increase

    return own_score, opponent_score


def print_history(history: History) -> None:
    """
    Prints a nice representation of a History object.
    
    Example:
    >>> history = History(
    ...     own_moves=[COOP, COOP, DEFECT, COOP, DEFECT, COOP],
    ...     opponent_moves=[DEFECT, DEFECT, DEFECT, COOP, COOP, DEFECT]
    ... )
    H ..x.x.
    A xxx..x
    # (with colors, that can't be shown here)    
    """
    coop_letter = "·"
    defect_letter = "×"
    def handle_line(lst):
        return "".join(f"\x1b[32m{coop_letter}\x1b[0m" if elem == Action.COOP else f"\x1b[31m{defect_letter}\x1b[0m" for elem in lst)
    
    print(
        "H " + handle_line(history.own_moves),
        "\n",
        "A " + handle_line(history.opponent_moves),
        sep=""
    )



if __name__ == "__main__":
    
    history = History(
        own_moves=[
            Action.COOP,
            Action.DEFECT,
            Action.COOP,
            Action.COOP,
            Action.COOP,
            Action.DEFECT,
            Action.DEFECT,
            Action.DEFECT,
            Action.DEFECT,
        ],
        opponent_moves=[
            Action.COOP,
            Action.COOP,
            Action.COOP,
            Action.DEFECT,
            Action.DEFECT,
            Action.COOP,
            Action.DEFECT,
            Action.DEFECT,
            Action.COOP,
        ],
    )
    
    print_history(history)