"""
Basically an evolution, but because
there's no mutation, "it's actually
an ecological simulation" (Derek, https://www.youtube.com/watch?v=mScpHTIi-kM&t=1045s)
"""
from utils import battle, Player, adjust_populations, Strategy#, save_scores_2_json, summary
from catalogue import EXAMPLE_SPECIES
import itertools as it
from tqdm import tqdm
from gui import App
import configparser
import random

#TODO implement the GUI
#app = App()
#app.mainloop()

config = configparser.ConfigParser()
config.read("config.ini")
starting_population = config.getint("SimulationParameters", "StartingPopulation")
_rounds_per_battle = config.getint("SimulationParameters", "RoundsPerBattle")
_rounds_per_battle_stddev = config.getint("SimulationParameters", "RoundsPerBattleStdDev")

if _rounds_per_battle_stddev * 4 > _rounds_per_battle:
    print("\x1b[0;33;40mWARNING\x1b[0m: stddev is a bit large, might cause negative rounds per battle.")

if _rounds_per_battle < 20:
    print("\x1b[0;33;40mWARNING\x1b[0m: rounds per battle is a bit small.")

def get_rounds():
    if _rounds_per_battle_stddev == 0:
        return _rounds_per_battle
    random_float = random.gauss(
        _rounds_per_battle,
        _rounds_per_battle_stddev
    )
    random_integer = round(random_float)
    if random_integer < 10:
        return 10
    return random_integer


POPULATIONS: dict[Strategy, int] = {
    species: starting_population
    for species in EXAMPLE_SPECIES.values()
}


for generation in it.count(1):

    population = [
        Player(species())
        for species, count in POPULATIONS.items()
        for _ in range(count)
    ]
    N = len(population)

    scores_this_round = {
        species: 0
        for species in EXAMPLE_SPECIES
    }

    # Battle everyone against everyone else
    num_rounds = N * (N-1) // 2
    for player1, player2 in tqdm(it.combinations(population, 2), total=num_rounds):
        
        score_1, score_2 = battle(player1, player2, rounds=get_rounds())

        scores_this_round[player1.strategy_name] += score_1
        scores_this_round[player2.strategy_name] += score_2


    # Size down to per-round score for ease of understanding
    AVG_SCORES_PER_ROUND = {
        species: score // (N-1)
        for species, score in scores_this_round.items()
    }


    # Size down cuz two of one species that gets 200 each isn't better than one of another species that gets 300,
    # but the current number shows 400 due to += even tho it's just because the population is larger, not
    # that each individual is stronger
    for species, score in AVG_SCORES_PER_ROUND.items():
        AVG_SCORES_PER_ROUND[species] = score // (POPULATIONS[species] or 1)

    # print(summary(AVG_SCORES_PER_ROUND))
    # save_scores_2_json(AVG_SCORES_PER_ROUND)
    POPULATIONS = adjust_populations(POPULATIONS, AVG_SCORES_PER_ROUND)
    # save_scores_2_json(POPULATIONS, filename="populations.json")

    # Continue or stop?
    if input(f"Generation {generation} complete. Enter to continue. [q] to stop.").lower() == "q":
        break



print("scores_this_round")
print("======")
print({species.__name__: score for species, score in AVG_SCORES_PER_ROUND.items()})
#save_scores_2_json(AVG_SCORES_PER_ROUND)

