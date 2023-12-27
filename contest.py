from species import EXAMPLE_SPECIES
from pprint import pprint
from utils import battle
import itertools



SCORES = {
    species.__name__: 0
    for species in EXAMPLE_SPECIES
}
_num_rounds = (len(EXAMPLE_SPECIES) * (len(EXAMPLE_SPECIES)-1)) // 2



for i, (species1, species2) in enumerate(itertools.combinations(EXAMPLE_SPECIES, 2), start=1):
    score_1, score_2 = battle(species1, species2, rounds=100)
    SCORES[species1.__name__] += score_1
    SCORES[species2.__name__] += score_2


assert i == _num_rounds, "Why wasn't there n(n-1)/2 rounds?"


AVG_SCORES_PER_ROUND = {
    species: score // (len(EXAMPLE_SPECIES)-1)
    for species, score in SCORES.items()
}


print("Scores")
print("======")
pprint(AVG_SCORES_PER_ROUND)
