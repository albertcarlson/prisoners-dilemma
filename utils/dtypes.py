"""
This file contains important, yet semi-ugly
/ abstract datatypes that are used throughout
the project. It is intended to only be imported
by other files in the project to ensure a clean
API.
"""
from __future__ import annotations
from collections.abc import MutableSequence
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import itertools as it
from enum import Enum
import configparser
import random



class Action(Enum):
    COOP: bool = False
    DEFECT: bool = True

    def __invert__(self):
        return Action(not self.value)



def _read_payoff_matrix(filename="config.ini") -> dict[tuple[Action, Action], tuple[int, int]]:
    """Reads the payoff matrix from the config file.
    Returns a dictionary of (Action, Action) -> (int, int) mappings.
    The payoff matrix is symmetric, so the only reason there is both
    an (COOP, DEFECT) and (DEFECT, COOP) is to make it easier to just do

    >>> _read_payoff_matrix()[(some_action, another_action)]
    
    for arbitrary some_action, another_action ∈ {COOP, DEFECT}."""    
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        (Action.COOP, Action.COOP): (int(config.get('PayoffMatrix', 'CoopCoop')), int(config.get('PayoffMatrix', 'CoopCoop'))),
        (Action.COOP, Action.DEFECT): (int(config.get('PayoffMatrix', 'CoopDefect')), int(config.get('PayoffMatrix', 'DefectCoop'))),
        (Action.DEFECT, Action.COOP): (int(config.get('PayoffMatrix', 'DefectCoop')), int(config.get('PayoffMatrix', 'CoopDefect'))),
        (Action.DEFECT, Action.DEFECT): (int(config.get('PayoffMatrix', 'DefectDefect')), int(config.get('PayoffMatrix', 'DefectDefect'))),
    }

PAYOFF_MATRIX = _read_payoff_matrix()



def _read_starting_population(filename="config.ini") -> int:
    """Reads the starting population from the config file."""
    config = configparser.ConfigParser()
    config.read(filename)
    return config.getint("SimulationParameters", "StartingPopulation")

STARTING_POPULATION = _read_starting_population()



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
    
    @property
    def score(self) -> tuple[float, float]:
        """Returns a tuple of (own_score, opponent_score) from a History object."""
        own_score = 0
        opponent_score = 0
        for own_move, opponent_move in self:
            
            own_increase, opponent_increase = PAYOFF_MATRIX[own_move, opponent_move]
            own_score += own_increase
            opponent_score += opponent_increase

        return own_score / len(self), opponent_score / len(self)  # Normalize score for useful comparison

    def __repr__(self) -> str:
        return f"History(own_moves={self.own_moves}, opponent_moves={self.opponent_moves})"

    def __str__(self) -> str:
        """
        Prints a nice representation of a History object.
        
        Example:
        >>> history = History(
        ...     own_moves=[COOP, COOP, DEFECT, COOP, DEFECT, COOP],
        ...     opponent_moves=[DEFECT, DEFECT, DEFECT, COOP, COOP, DEFECT]
        ... )
        H ··×·×·
        A ×××··×
        # (with colors, that can't be shown here)    
        """
        coop_letter = "·"
        defect_letter = "×"
        def handle_line(lst):
            return "".join(f"\x1b[32m{coop_letter}\x1b[0m" if elem == Action.COOP else f"\x1b[31m{defect_letter}\x1b[0m" for elem in lst)
        
        return "H " + handle_line(self.own_moves) + "\n" + "A " + handle_line(self.opponent_moves)



class Strategy(ABC):
    @abstractmethod
    def decide(self, history: History) -> Action:
        pass



class Player:
    def __init__(self, strategy: Strategy):
        self.strategy_name = strategy.__class__.__name__
        self.strategy = strategy
        self.most_recent_score = 0
        self.age = 0

    def make_decision(self, history):
        return self.strategy.decide(history)
    
    def grow_older(self):
        self.age += 1

    def replicate(self):
        return Player(self.strategy)
    
    def change_strategy(self, new_strategy: Strategy):
        self.strategy = new_strategy
        self.strategy_name = new_strategy.__class__.__name__

    def battle(self, opponent: Player, *, rounds: int = 100) -> tuple[int, int]:
        """
        Battles two `Player`s against each other for `rounds` rounds,
        returning the scores for each player (normalized by the number of rounds
        so more rounds doesn't equate to higher scores).
        """
        history = History()

        for _ in range(rounds):
            decision1 = self.make_decision(history)
            decision2 = opponent.make_decision(~history)  # Inverted history, because for the opponent, our moves are their moves etc.

            assert decision1 in (Action.COOP, Action.DEFECT), f"WHAT, {self} made this move: {decision1} against {opponent}, who made {decision2}.\n{history}"
            assert decision2 in (Action.COOP, Action.DEFECT), f"WHAT, {opponent} made this move: {decision2} against {self}, who made {decision1}.\n{history}"

            history.append(
                own_move=decision1,
                opponent_move=decision2
            )

        assert len(history) == rounds
                
        return history.score
        
    def __repr__(self):
        return f"<Player object at {hex(id(self))} using {self.strategy_name}>"



def battle(
        player1: Player,
        player2: Player,
        *,
        rounds: int = 100,
        debug: bool = False
    ) -> tuple[int, int]:
    """
    Battles two `Player`s against each other for `rounds` rounds,
    returning the scores for each player (normalized by the number of rounds
    so more rounds doesn't equate to higher scores).
    
    This function is just syntactic sugar for `player1.battle(player2)`,
    so it appears symmetric, i.e. `battle(player1, player2)`.
    """
    return player1.battle(player2, rounds=rounds)



@dataclass
class Population:
    # Double list due to time series data
    players: list[list[Player]] = field(default_factory=list)
    __scores: list[list[float]] = field(default_factory=list)

    @property
    def population_counts(self) -> dict[str, int]:
        return {
            player.strategy_name: [
                strat.strategy_name for strat in self.players[-1]
            ].count(player.strategy_name)
            for player in self.players[-1]
        }
    
    @property
    def generation(self) -> int:
        return len(self.__scores[-1])
    
    @property
    def population_size(self) -> int:
        return len(self.players[-1])

    def do_generation(
        self,
        matchup_rate: float = 1.0,
        # payoff_matrix,  # TODO: Support payoff matrix that isn't just the global constant loaded from config.ini
        rounds: int = 50,
        overall_food: int = 1_000,
        adjust_populations: bool = True
    ) -> None:
        """
        Does one generation in a round-robin tournament style.
        
        - However, a given matchup only happens with `matchup_rate` probability.
        So if `matchup_rate` is 1.0, all (N choose 2) matchups happen, where
        N is the population size. While if `matchup_rate` is 0.5, around half
        of the matchups occur, and every player is expected to meet (N-1)/2 others.
        Reduce to speed up a generation.

        - The `rounds` are how long a game lasts: For each matchup, the players
        play `rounds` rounds of the prisoner's dilemma game, each remembering the
        history of the other and play accordingly (in accordance with their `Strategy`).

        - `overall_food` is the desired convergence of the population size. (NOT QUITE: FIX THIS EXPLANATION) This is used
        to adjust the population size after each generation proportional to their score
        times the `overall_food` divided by the current population size.
        """
        # Step 1. Battle everyone against everyone (each matchup with probability `matchup_rate`)
        self.__scores.append([0 for _ in self.players[-1]])

        for matchup, ((p1_idx, player1), (p2_idx, player2)) in enumerate(it.combinations(enumerate(self.players), 2), start=1):
            if random.random() > matchup_rate:
                continue
            
            score1, score2 = battle(player1, player2, rounds=rounds)  # FIXME: Circular import
            
            self.__scores[-1][p1_idx] += score1
            self.__scores[-1][p2_idx] += score2

        assert matchup == self.population_size * (self.population_size - 1) // 2, "Why wasn't there (N choose 2) battles?"

        # Step 2. Normalize scores
        # TODO: here we should normalize by matchup rate and population size
        # The History object already normalized by rounds
        expected_matchups = (self.population_siz - 1) * matchup_rate
        self.__scores[-1] = [score / expected_matchups for score in self.__scores[-1]]

        # Step 3. Adjust population sizes
        if adjust_populations:
            self.__adjust_populations(overall_food)

    def __adjust_populations(self, overall_food: int) -> None:
        """
        Adjusts the population size based on the scores of the players.
        The adjustment is proportional to the score of the player times the
        `overall_food` parameter, divided by the current population size.
        """
        if len(self.players) == len(self.__scores):
            raise ValueError("Can't adjust populations before a generation has been run.")
        assert len(self.players) == len(self.__scores) - 1, "Why is the population size not one more than the same as the number of __scores?"
        pass  # TODO: Adjust populations based on __scores and overall_food


if __name__ == "__main__":

    class AlwaysCoop(Strategy):
        def decide(self, history: History) -> Action:
            return Action.COOP

    pop = Population([[Player(AlwaysCoop()), Player(AlwaysCoop()), Player(AlwaysCoop()), Player(AlwaysCoop())]])
    pop.do_generation()
    pop.do_generation()
    print(pop.generation)
    pop.do_generation()
    pop.do_generation()
    print(pop.generation)


    print(pop.population_counts)