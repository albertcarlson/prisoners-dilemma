"""
Library for various helper tools.
E.g. getting the curent scores,
printing moves in a nice way,
adjusting populations, etc.
"""

# from dict_zip import dict_zip
# import json




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


from utils.dtypes import Action, History, Player
import random


def random_action() -> Action:
    """Simple utility function to avoid
    having to type Action(random.getrandbits(1))."""
    return Action(random.getrandbits(1))


def battle(
    player1: Player,
    player2: Player,
    *,
    rounds: int = 100,
    debug: bool = False
) -> tuple[int, int]:
    

    history = History()

    for _ in range(rounds):
        decision1 = player1.make_decision(history)
        decision2 = player2.make_decision(~history)  # Inverted history, because for the opponent, our moves are their moves etc.

        assert decision1 in (Action.COOP, Action.DEFECT), f"WHAT, {player1} made this move: {decision1} against {player2}, who made {decision2}.\n{history}"
        assert decision2 in (Action.COOP, Action.DEFECT), f"WHAT, {player2} made this move: {decision2} against {player1}, who made {decision1}.\n{history}"

        history.append(
            own_move=decision1,
            opponent_move=decision2
        )

    assert len(history) == rounds
    
    if debug:
        print(history, file=open("debug.txt", "a"))
    
    return history.score


