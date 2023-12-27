"""
Basically an evolution, but because
there's no mutation, "it's actually
an ecological simulation" (Derek, https://www.youtube.com/watch?v=mScpHTIi-kM&t=1045s)
"""
from utils import battle, Player#, adjust_populations, save_scores_2_json, summary
from species import EXAMPLE_SPECIES
import itertools as it
from tqdm import tqdm
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
starting_population = config.getint('DEFAULT', 'StartingPopulation')


POPULATIONS = {
    species: starting_population
    for species in EXAMPLE_SPECIES
}


for generation in it.count(1):

    population = [
        Player(species)
        for species, count in POPULATIONS.items()
        for _ in range(count)
    ]
    population_size = len(population)

    scores_this_round = {
        species: 0
        for species in EXAMPLE_SPECIES
    }

    # Battle everyone against everyone else
    _num_rounds = population_size * (population_size-1) // 2
    for player1, player2 in tqdm(it.combinations(population, 2), total=_num_rounds):
        
        score_1, score_2 = battle(player1, player2, rounds=100)

        scores_this_round[player1] += score_1
        scores_this_round[player2] += score_2


    # Size down to per-round score for ease of understanding
    AVG_SCORES_PER_ROUND = {
        species: score // (population_size-1)
        for species, score in scores_this_round.items()
    }


    # Size down cuz two of one species that gets 200 each isn't better than one of another species that gets 300,
    # but the current number shows 400 due to += even tho it's just because the population is larger, not
    # that each individual is stronger
    for species, score in AVG_SCORES_PER_ROUND.items():
        AVG_SCORES_PER_ROUND[species] = score // (POPULATIONS[species] or 1)

    print(summary(AVG_SCORES_PER_ROUND))
    save_scores_2_json(AVG_SCORES_PER_ROUND)
    POPULATIONS = adjust_populations(POPULATIONS, AVG_SCORES_PER_ROUND)
    save_scores_2_json(POPULATIONS, filename="populations.json")

    # Continue or stop?
    stop = input(f"Generation {generation} complete. Enter to continue. [q] to stop.").lower() == "q"
    if stop:
        break



print("scores_this_round")
print("======")
print({species.__name__: score for species, score in AVG_SCORES_PER_ROUND.items()})
save_scores_2_json(AVG_SCORES_PER_ROUND)

