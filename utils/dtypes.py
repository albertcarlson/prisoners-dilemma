"""
This file contains important, yet semi-ugly / abstract datatypes that
are used throughout the project, such as Strategy, Player, Population,
Action and History. It is intended to only be imported by other files
in the project to ensure a clean API.
"""
from __future__ import annotations
from collections.abc import MutableSequence
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import itertools as it
from enum import Enum
import configparser
import random



def round_probabilistically(x: float, /) -> int:
    """
    Rounds a float to an integer probabilistically.
    For example, 3.75 would be rounded to 4 with 75% probability,
    and 3 with 25% probability.
    """
    q, r = divmod(x, 1)
    return int(q) + (random.random() < r)



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
    def __init__(self, strategy: Strategy, *, most_recent_score: int = 0, age: int = 0) -> None:
        self.strategy_name = strategy.__class__.__name__
        self.strategy = strategy
        self.most_recent_score = most_recent_score
        self.age = age

    def make_decision(self, history) -> Action:
        return self.strategy.decide(history)
    
    def get_offspring(
            self, 
            offspring: int, 
            *, 
            mutation_strategies: list[Strategy] | None = None, 
            mutation_probability: float = 0
    ) -> list[Player]:
        """
        Returns a list of `Player`s that are offspring of this player
        for the new generation. Note that for convenience, this includes
        the player itself aged by one year, and `offspring-1` new players
        with age 0, so we can easily get the new generation of players.

        If `offspring` is 0, an empty list is returned, since the player
        didn't survive.

        If `offspring` is 1, only the player itself is returned, aged by one year,
        as it survived but didn't reproduce.
        """
        if not isinstance(offspring, int):
            raise TypeError(f"Expected `offspring` to be an integer, but got {type(offspring)}")
        if offspring < 0:
            raise ValueError(f"Expected `offspring` to be a positive integer, but got {offspring}")
        
        if offspring == 0:
            return []
        
        players = [Player(self.strategy, age=self.age + 1)]
        players.extend(
            Player(self.strategy, age=0)
            for _ in range(offspring-1)
        )
        for player in players[1:]:
            if random.random() < mutation_probability:
                player.mutate(mutation_strategies)
        return players
    
    def change_strategy(self, new_strategy: Strategy) -> None:
        self.strategy = new_strategy
        self.strategy_name = new_strategy.__class__.__name__

    def mutate(self, mutation_strategies: list[Strategy]) -> None:
        """
        Mutates the player's strategy in-place to a random, new
        strategy chosen from the `mutation_strategies` list. It
        might "mutate back" to its current strategy as well, but
        this shouldn't matter too much.
        """
        self.change_strategy(random.choice(mutation_strategies))

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
        
    def __repr__(self) -> str:
        return f"<Player object at {hex(id(self))} using {self.strategy_name}>"



def battle(
        player1: Player,
        player2: Player,
        *,
        rounds: int = 100,
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
    """
    Simulates an entire population/society of `Player`s each with their
    own `Strategy` that interact and get offspring. This `Population` class
    comes with a `do_generation` method that simulates one generation of
    the population battling and reproducing. You can specify mutation
    probabilities and more to play with the simulation.

    In that way, you can say that this class is the core of the ecological
    simulation.

    ## Example
    >>> class AlwaysCoop(Strategy):
    >>>     def decide(self, history: History) -> Action:
    >>>         return Action.COOP
    >>> class AlwaysDefect(Strategy):
    >>>     def decide(self, history: History) -> Action:
    >>>         return Action.DEFECT
    >>> pop = Population([[Player(AlwaysCoop()), Player(AlwaysCoop()), Player(AlwaysCoop())]])
    >>> for gen in range(20):
    >>>     print(pop.generation, pop.population_counts, pop.population_size, pop.population_average_age)
    >>>     pop.do_generation(overall_food=20, mutation_probability=0.1, mutation_strategies=[AlwaysDefect(), AlwaysCoop()])

    The example above starts with 3 cooperaters that should grow in numbers within a few
    generations. However, sooner or later, since mutation_probability is 0.1, a defector
    will appear and the population will be taken over by defectors, and also shrink since
    they're "less efficient overall" (as long as you specify the DEFECT-DEFECT reward in
    the payoff matrix to be  less than the COOP-COOP reward). Occasionally, a coop will
    re-appear due to mutation, but it will be outcompeted by the defectors. You might also
    see the average age decline briefly as the defectors take over because all the old coops
    die out and the new defectors are young.

    This is a simple example that demonstrates the prisoner's dilemma and the tragedy of
    the commons.
    """
    # Double list due to time series data (we want to keep all generations)
    players: list[list[Player]] = field(default_factory=list)

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
        return len(self.players) - 1
    
    @property
    def population_size(self) -> int:
        return len(self.players[-1])
    
    @property
    def population_average_age(self) -> float:
        return sum(player.age for player in self.players[-1]) / self.population_size

    def do_generation(
        self,
        matchup_rate: float = 1.0,
        # payoff_matrix,  # TODO: Support payoff matrix that isn't just the global constant loaded from config.ini
        rounds: int = 50,
        overall_food: int = 1_000,
        adjust_populations: bool = True,
        **kwargs
    ) -> None:
        """
        Does one generation in a round-robin tournament style.
        
        - However, a given matchup only happens with `matchup_rate` probability.
          So if `matchup_rate` is 1.0, all (N choose 2) matchups happen, where
          N is the population size. While if `matchup_rate` is 0.5, around half
          of the matchups occur, and every player is expected to meet (N-1)/2 others.
          Reduce this variable to speed up a generation.

        - The `rounds` are how long a game lasts: For each matchup, the players
          play `rounds` rounds of the prisoner's dilemma game, each remembering the
          history of the other and play accordingly (in accordance with their `Strategy`).

        - `overall_food` is used to adjust the population size after each generation
          based on each player's score. This parameter is correlated with the desired
          convergence of the population size. More precisely, the population size
          approximately converges to the average score of the players times the overall food.
          I.e. a whole population of altruistic players that always cooperate (and who might
          get an average score each of 3 each) will converge to 3 times the food since they
          "get more out of it" than a whole population of defectors (that might only get 1
          on average) and thus only a population size of 1 times the food.

        - `**kwargs` are passed to the `Player.get_offspring` method. As of
          writing, you can therefore supply `mutation_strategies` and `mutation_probability`,
          but keep in touch with the documentation of the `Player.get_offspring` method.
        """
        # Step 1. Battle everyone against everyone (each matchup with probability `matchup_rate`)
        expected_matchups = (self.population_size - 1) * matchup_rate

        for match_num, (player1, player2) in enumerate(it.combinations(self.players[-1], 2), start=1):
            
            if random.random() > matchup_rate:
                continue
            
            score1, score2 = battle(player1, player2, rounds=rounds)
            
            player1.most_recent_score += score1 / expected_matchups
            player2.most_recent_score += score2 / expected_matchups

        assert match_num == self.population_size * (self.population_size - 1) // 2, "Why wasn't there (N choose 2) battles?"
        
        # Step 2. Adjust population sizes
        if adjust_populations:
            self.__adjust_populations(overall_food, **kwargs)

    def __adjust_populations(self, overall_food: int, **kwargs) -> None:
        """
        Adjusts the population size based on the scores of the players.

        The adjustment is proportional to the score of the player times the
        `overall_food` parameter, divided by the current population size.

        Appends the new generation of players to the `players` list.

        **kwargs are passed to the `Player.get_offspring` method. As of
        writing, you can therefore supply `mutation_strategies` and `mutation_probability`,
        but keep in touch with the documentation of the `Player.get_offspring` method.
        """
        new_generation = []
        
        for player in self.players[-1]:
            # Normalize scores and use them to calculate offspring.
            # History object already normalizes by number of rounds,
            # so we just need to divide by the expected number of matchups,
            # multiply by the overall food, and divide by the population size.
            # This formula arises from the desired population size convergence.
            offspring = round_probabilistically(player.most_recent_score * overall_food / self.population_size)
            new_generation.extend(player.get_offspring(offspring, **kwargs))

        self.players.append(new_generation)



if __name__ == "__main__":
    
    import warnings
    warnings.warn("This file is not intended to be run as a script. Please import it elsewhere. This is just for testing.")
    
    class AlwaysCoop(Strategy):
        def decide(self, history: History) -> Action:
            return Action.COOP
        
    class AlwaysDefect(Strategy):
        def decide(self, history: History) -> Action:
            return Action.DEFECT

    pop = Population([[Player(AlwaysCoop()), Player(AlwaysCoop()), Player(AlwaysCoop()), Player(AlwaysCoop())]])
    
    for _ in range(20):
        print(pop.generation, pop.population_counts, pop.population_size, pop.population_average_age)
        pop.do_generation(overall_food=20, mutation_probability=0.1, mutation_strategies=[AlwaysDefect(), AlwaysCoop()])