"""
Basically an evolution, but because
there's no mutation, "it's actually
an ecological simulation" (Derek, https://www.youtube.com/watch?v=mScpHTIi-kM&t=1045s)
"""
from utils import battle, Player, adjust_populations, Strategy#, save_scores_2_json, summary
from catalogue import EXAMPLE_SPECIES as SPECIES
from math import isclose
import itertools as it
import configparser
import random


config = configparser.ConfigParser()
config.read("config.ini")
_starting_population = config.getint("SimulationParameters", "StartingPopulation")
_rounds_per_battle = config.getint("SimulationParameters", "RoundsPerBattle")
_rounds_per_battle_stddev = config.getint("SimulationParameters", "RoundsPerBattleStdDev")
_adjustment_noise = config.getfloat("SimulationParameters", "PopulationAdjustmentEpsilonStdDev")


if _rounds_per_battle_stddev * 4 > _rounds_per_battle:
    print("\x1b[0;33;40mWARNING\x1b[0m: stddev is a bit large, might cause negative rounds per battle.")



class MODEL_Simulation:
    def __init__(self, species: dict[str, int] = SPECIES, matchup_factor: float = 1.0):
        """
        species: dict[str, int]
            species_name ↦ population
            e.g. {"TitForTat": 10, "Random": 10}
        Default is the example species from catalogue/example_species.py

        matchup_factor: float ∈ [0, 1]
            0: no battles at all
            1: everyone fights everyone in each generation
            0.5: randomly, around half of the total (N choose 2) battles are fought each generation
        """
        self.generation = 0
        self.matchup_factor = matchup_factor  # TODO! Implement this in battle()
        if matchup_factor != 1:
            raise NotImplementedError("matchup_factor is not implemented yet")
        if not 0 <= matchup_factor <= 1:
            raise ValueError(f"matchup_factor must be in [0, 1], but was {matchup_factor}.")
        self.SPECIES = species

        self.species_counts: dict[str, int] = {
            species_name: _starting_population
            for species_name in self.SPECIES.keys()
        }
        self.population: list[Player] = self._population_from_counts(self.species_counts)
        self.population_size = len(self.population)

        assert self.population_size == sum(self.species_counts.values()) == _starting_population * len(self.SPECIES)
        
        # For progress bar visualization
        self.progress = 0.0


    def do_generation(self):
        self.generation += 1
        self._battle_everyone_against_everyone()
        self._adjust_populations()


    def _battle_everyone_against_everyone(self):
        
        # Player ↦ score
        self.scores_this_generation: dict[Player, int] = {
            player: 0
            for player in self.population
        }

        self.progress = 0
        num_rounds = self.population_size * (self.population_size-1) // 2
        for player1, player2 in it.combinations(self.population, 2):
            self.progress += 1 / num_rounds
            
            score_1, score_2 = battle(player1, player2, rounds=max(1, round(random.gauss(mu=_rounds_per_battle, sigma=_rounds_per_battle_stddev))))
            # NOTE: If self.get_rounds() by randomness evaluates lower for some player, they
            # end up having a smaller score overall. This can be fine, due to randomness but
            # it's good to be aware of it.

            self.scores_this_generation[player1] += score_1
            self.scores_this_generation[player2] += score_2
        
        assert isclose(self.progress, 1)


    def _adjust_populations(self):
        
        total_score = sum(self.scores_this_generation.values())

        species_scores: dict[str, int] = {
            player.strategy_name: 0
            for player in self.population
        }
        # Take sum of all folks of a species to get total species scores
        for player, score in self.scores_this_generation.items():
            species_scores[player.strategy_name] += score
        # Adjust down
        for species_name, score in species_scores.items():
            species_scores[species_name] = score // self.species_counts[species_name]
        
        # Now adjust the populations
        for species_name, score in species_scores.items():
            # keep total population approx constant
            self.species_counts[species_name] = round(
                self.species_counts[species_name] * (score / total_score)
                + random.gauss(mu=0, sigma=_adjustment_noise)
            )
        
        self.population = self._population_from_counts(self.species_counts)
        self.population_size = sum(self.populations.values())
    

    def _population_from_counts(self, counts: dict[Strategy, int]) -> list[Player]:
        return [
            Player(Species())
            for Species, count in counts.items()
            for _ in range(count)
        ]





# for generation in it.count(1):

   
#     # Size down to per-round score for ease of understanding
#     AVG_SCORES_PER_ROUND = {
#         species: score // (N-1)
#         for species, score in scores_this_round.items()
#     }


#     # Size down cuz two of one species that gets 200 each isn't better than one of another species that gets 300,
#     # but the current number shows 400 due to += even tho it's just because the population is larger, not
#     # that each individual is stronger
#     for species, score in AVG_SCORES_PER_ROUND.items():
#         AVG_SCORES_PER_ROUND[species] = score // (POPULATIONS[species] or 1)

#     # print(summary(AVG_SCORES_PER_ROUND))
#     # save_scores_2_json(AVG_SCORES_PER_ROUND)
#     POPULATIONS = adjust_populations(POPULATIONS, AVG_SCORES_PER_ROUND)
#     # save_scores_2_json(POPULATIONS, filename="populations.json")

#     # Continue or stop?
#     if input(f"Generation {generation} complete. Enter to continue. [q] to stop.").lower() == "q":
#         break



# print("scores_this_round")
# print("======")
# print({species.__name__: score for species, score in AVG_SCORES_PER_ROUND.items()})
# #save_scores_2_json(AVG_SCORES_PER_ROUND)

