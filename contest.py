"""
A single "generation" / "iteration" of the contest.
Simply battles everyone once against everyone else,
and figures out the scores for each, resulting in a 
leaderboard.
"""
from catalogue import EXAMPLE_SPECIES
from utils import battle, Player
from pprint import pprint
import itertools as it


# EXAMPLE_SPECIES = {
#     key: val
#     for key, val in
#     EXAMPLE_SPECIES.items()
#     if key in ("TitForTat", "TitForTwoTats")
# }


SCORES = {
    species: 0
    for species in EXAMPLE_SPECIES
}
_num_rounds = (len(EXAMPLE_SPECIES) * (len(EXAMPLE_SPECIES)-1)) // 2


players = [
    Player(strategy())
    for strategy in EXAMPLE_SPECIES.values()
]


for idx, (player1, player2) in enumerate(it.combinations(players, 2), start=1):
    
    score_1, score_2 = battle(player1, player2, rounds=100)
    
    SCORES[player1.strategy_name] += score_1
    SCORES[player2.strategy_name] += score_2


assert idx == _num_rounds, "Why wasn't there n(n-1)/2 rounds?"


AVG_SCORES_PER_ROUND = {
    species: score // (len(EXAMPLE_SPECIES)-1)
    for species, score in SCORES.items()
}


print("Scores")
print("======")
pprint(AVG_SCORES_PER_ROUND)

