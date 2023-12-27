"""
Basically an evolution, but because
there's no mutation, "it's actually
an ecological simulation" (Derek, https://www.youtube.com/watch?v=mScpHTIi-kM&t=1045s)
"""
from utils import battle, adjust_populations, save_scores_2_json, summary
from species import SPECIES
from tqdm import tqdm
import itertools


POPULATIONS = {
    species: 5  # Start with 5 of each species
    for species in SPECIES
}



for generation in itertools.count(1):

    populations_list = [
        species
        for species, count in POPULATIONS.items()
        for _ in range(count)
    ]

    scores_this_round = {
        species: 0
        for species in SPECIES
    }

    # battle everyone against everyone else
    _num_rounds = len(populations_list) * (len(populations_list)-1) // 2
    for species1, species2 in tqdm(itertools.combinations(populations_list, 2), total=_num_rounds):
        score_1, score_2 = battle(species1, species2, rounds=100)
        scores_this_round[species1] += score_1
        scores_this_round[species2] += score_2


    # size down to per-round score for clarity
    AVG_SCORES_PER_ROUND = {
        species: score // (len(populations_list)-1)
        for species, score in scores_this_round.items()
    }
    # size down cuz two of one species that gets 200 each isn't better than one of another species that gets 300,
    # but the current number shows 400 due to += even tho it's just because the population is larger, not
    # that each individual is stronger
    for species, score in AVG_SCORES_PER_ROUND.items():
        AVG_SCORES_PER_ROUND[species] = score // (POPULATIONS[species] or 1)

    print(summary(AVG_SCORES_PER_ROUND))
    save_scores_2_json(AVG_SCORES_PER_ROUND)
    POPULATIONS = adjust_populations(POPULATIONS, AVG_SCORES_PER_ROUND)
    save_scores_2_json(POPULATIONS, filename="populations.json")
    stop = input(f"Generation {generation} complete. Enter to continue. [q] to stop.").lower() == "q"
    if stop:
        break



print("scores_this_round")
print("======")
print({species.__name__: score for species, score in AVG_SCORES_PER_ROUND.items()})
save_scores_2_json(AVG_SCORES_PER_ROUND)

