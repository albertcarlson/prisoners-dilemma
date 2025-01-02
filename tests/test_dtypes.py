from utils import Strategy, Action, History, round_probabilistically, PayoffMatrix, Player, flatten
from collections.abc import MutableSequence
import pytest


@pytest.fixture
def payoff_matrix_1():
    return PayoffMatrix(3, 0, 5, 1)

@pytest.fixture
def payoff_matrix_2():
    return PayoffMatrix(5, -5, 10, -10)

@pytest.fixture
def payoff_matrix_3():
    return PayoffMatrix.from_config("config.ini")


def test_payoff_matrix(payoff_matrix_1, payoff_matrix_2, payoff_matrix_3):
    # Make sure all 4 action combinations are in the payoff matrix
    for payoff_dict in [payoff_matrix_1.as_dict(), payoff_matrix_2.as_dict(), payoff_matrix_3.as_dict()]:
        # Old legacy code for the dictionaries
        assert len(payoff_dict) == 4
        assert (Action.COOP, Action.COOP) in payoff_dict, f"Didn't find COOP, COOP in payoff matrix"
        assert (Action.COOP, Action.DEFECT) in payoff_dict, f"Didn't find COOP, DEFECT in payoff matrix"
        assert (Action.DEFECT, Action.COOP) in payoff_dict, f"Didn't find DEFECT, COOP in payoff matrix"
        assert (Action.DEFECT, Action.DEFECT) in payoff_dict, f"Didn't find DEFECT, DEFECT in payoff matrix"
        # Assert types are correct
        assert isinstance(payoff_dict, dict), f"payoff_dict should be a dict, but was {type(payoff_dict)}"
        assert isinstance(payoff_dict[(Action.COOP, Action.COOP)], tuple), f"payoff_dict[(Action.COOP, Action.COOP)] should be a tuple, but was {type(payoff_dict[(Action.COOP, Action.COOP)])}"
        assert isinstance(payoff_dict[(Action.COOP, Action.DEFECT)], tuple), f"payoff_dict[(Action.COOP, Action.DEFECT)] should be a tuple, but was {type(payoff_dict[(Action.COOP, Action.DEFECT)])}"
        assert isinstance(payoff_dict[(Action.DEFECT, Action.COOP)], tuple), f"payoff_dict[(Action.DEFECT, Action.COOP)] should be a tuple, but was {type(payoff_dict[(Action.DEFECT, Action.COOP)])}"
        assert isinstance(payoff_dict[(Action.DEFECT, Action.DEFECT)], tuple), f"payoff_dict[(Action.DEFECT, Action.DEFECT)] should be a tuple, but was {type(payoff_dict[(Action.DEFECT, Action.DEFECT)])}"
        # Assert length of tuples is correct
        assert len(payoff_dict[(Action.COOP, Action.COOP)]) == 2, f"payoff_dict[(Action.COOP, Action.COOP)] should be a tuple of length 2, but was {len(payoff_dict[(Action.COOP, Action.COOP)])}"
        assert len(payoff_dict[(Action.COOP, Action.DEFECT)]) == 2, f"payoff_dict[(Action.COOP, Action.DEFECT)] should be a tuple of length 2, but was {len(payoff_dict[(Action.COOP, Action.DEFECT)])}"
        assert len(payoff_dict[(Action.DEFECT, Action.COOP)]) == 2, f"payoff_dict[(Action.DEFECT, Action.COOP)] should be a tuple of length 2, but was {len(payoff_dict[(Action.DEFECT, Action.COOP)])}"
        assert len(payoff_dict[(Action.DEFECT, Action.DEFECT)]) == 2, f"payoff_dict[(Action.DEFECT, Action.DEFECT)] should be a tuple of length 2, but was {len(payoff_dict[(Action.DEFECT, Action.DEFECT)])}"

    assert payoff_matrix_1.get_reward(Action.COOP, Action.COOP) == (3, 3)
    assert payoff_matrix_1.get_reward(Action.COOP, Action.DEFECT) == (0, 5)
    assert payoff_matrix_1.get_reward(Action.DEFECT, Action.COOP) == (5, 0)
    assert payoff_matrix_1.get_reward(Action.DEFECT, Action.DEFECT) == (1, 1)

    assert payoff_matrix_2.get_reward(Action.COOP, Action.COOP) == (5, 5)
    assert payoff_matrix_2.get_reward(Action.COOP, Action.DEFECT) == (-5, 10)
    assert payoff_matrix_2.get_reward(Action.DEFECT, Action.COOP) == (10, -5)
    assert payoff_matrix_2.get_reward(Action.DEFECT, Action.DEFECT) == (-10, -10)


def test_action():
    # Make sure the enum has exactly 2 values, COOP and DEFECT
    assert len(Action) == 2, f"Action should have exactly 2 values, but had {len(Action)}"
    assert Action.COOP in Action, f"Action.COOP should be in Action, but wasn't"
    assert Action.DEFECT in Action, f"Action.DEFECT should be in Action, but wasn't"


def test_history():
    history = History()

    # Make sure the two fields are called own_moves and opponent_moves
    assert hasattr(history, "own_moves"), f"history should have a field called own_moves, but didn't"
    assert hasattr(history, "opponent_moves"), f"history should have a field called opponent_moves, but didn't"
    
    # Make sure they are lists
    assert isinstance(history.own_moves, MutableSequence), f"history.own_moves should be a list, but was {type(history.own_moves)}"
    assert isinstance(history.opponent_moves, MutableSequence), f"history.opponent_moves should be a list, but was {type(history.opponent_moves)}"
    
    # Test the 6 methods: append, __len__, __iter__, __invert__, score, __repr__
    # append and __len__
    history.append(Action.COOP, Action.DEFECT)
    assert len(history.own_moves) == 1, f"History.own_moves should have length 1, but was {len(history.own_moves)}"
    assert len(history.opponent_moves) == 1, f"History.opponent_moves should have length 1, but was {len(history.opponent_moves)}"
    assert len(history) == 1, f"History should have length 1, but was {len(history)}"
    assert history.own_moves[0] == Action.COOP, f"History.own_moves[0] should be Action.COOP, but was {history.own_moves[0]}"
    assert history.opponent_moves[0] == Action.DEFECT, f"History.opponent_moves[0] should be Action.DEFECT, but was {history.opponent_moves[0]}"

    # __invert__
    history = ~history
    assert len(history.own_moves) == 1, f"History.own_moves should have length 1, but was {len(history.own_moves)}"
    assert len(history.opponent_moves) == 1, f"History.opponent_moves should have length 1, but was {len(history.opponent_moves)}"
    assert len(history) == 1, f"History should have length 1, but was {len(history)}"
    assert history.own_moves[0] == Action.DEFECT, f"History.own_moves[0] should be Action.DEFECT, but was {history.own_moves[0]}"
    assert history.opponent_moves[0] == Action.COOP, f"History.opponent_moves[0] should be Action.COOP, but was {history.opponent_moves[0]}"

    for i, move in enumerate(history, start=1):
        assert move == (Action.DEFECT, Action.COOP), f"History should be iterable, but the {i}th element was {move}"

    assert i == 1

    # score
    # (Tested in another file)

    expected = "History(own_moves=[<Action.DEFECT: True>], opponent_moves=[<Action.COOP: False>])"
    assert repr(history) == expected, f"History.__repr__ should be '{expected}', but was {repr(history)}"


def test_round_probabilistically():
    for i in range(-5, 5):
        assert round_probabilistically(i) == i
        assert round_probabilistically(i + 0.5) in [i, i+1]


@pytest.fixture
def player_coop():
    class AlwaysCoop(Strategy):
        def decide(self, history: History) -> Action:
            return Action.COOP
    
    return Player(AlwaysCoop())


@pytest.fixture
def player_defect():
    class AlwaysDefect(Strategy):
        def decide(self, history: History) -> Action:
            return Action.DEFECT
    
    return Player(AlwaysDefect())


@pytest.fixture
def coop_class():
    class AlwaysCoop(Strategy):
        def decide(self, history: History) -> Action:
            return Action.COOP
    
    return AlwaysCoop


@pytest.fixture
def defect_class():
    class AlwaysDefect(Strategy):
        def decide(self, history: History) -> Action:
            return Action.DEFECT
    
    return AlwaysDefect


def test_player_basic_properties(player_coop, player_defect, payoff_matrix_3):
    assert player_coop.strategy.decide(None) == Action.COOP
    assert player_defect.strategy.decide(None) == Action.DEFECT

    assert player_coop.strategy_name == "AlwaysCoop"
    assert player_defect.strategy_name == "AlwaysDefect"

    assert player_coop.age == 0
    assert player_defect.age == 0

    assert player_coop.most_recent_score == 0
    assert player_defect.most_recent_score == 0

    score1, score2 = player_coop.battle(player_defect, rounds=17)
    # TODO! CHANGE THIS, BECAUSE THE battle METHOD WILL IN THE FUTURE NOT
    # NECESSARILY USE payoff_matrix_3 (the one from config.ini)
    assert score1 == payoff_matrix_3.as_dict()[(Action.COOP, Action.DEFECT)][0]
    assert score2 == payoff_matrix_3.as_dict()[(Action.COOP, Action.DEFECT)][1]

def test_player_offspring(player_coop, player_defect, coop_class, defect_class):
    offspring = player_coop.get_offspring(2)
    assert len(offspring) == 2
    assert offspring[0].strategy.decide(None) == Action.COOP
    assert offspring[1].strategy.decide(None) == Action.COOP
    assert offspring[0].strategy_name == "AlwaysCoop"
    assert offspring[1].strategy_name == "AlwaysCoop"
    assert offspring[0].age == 1  # Ensure it has aged
    assert offspring[1].age == 0
    assert offspring[0].most_recent_score == 0
    assert offspring[1].most_recent_score == 0

    offspring = player_defect.get_offspring(0)
    assert len(offspring) == 0
    
    with pytest.raises(ValueError):
        player_coop.get_offspring(-1)
    
    with pytest.raises(TypeError):
        player_coop.get_offspring(0.5)

    # Test offspring with mutation (equal to 1)
    offspring = player_coop.get_offspring(1, mutation_strategies=[coop_class(), defect_class()], mutation_probability=1)
    assert len(offspring) == 1
    assert offspring[0].strategy.decide(None) == Action.COOP
    assert offspring[0].strategy_name == "AlwaysCoop"
    assert offspring[0].age == 1  # Ensure it has aged

    offspring = player_defect.get_offspring(3, mutation_strategies=[coop_class()], mutation_probability=1)
    assert len(offspring) == 3
    assert offspring[0].strategy.decide(None) == Action.DEFECT  # Parent is still the same
    assert offspring[1].strategy.decide(None) == Action.COOP    # Child 1 has mutated
    assert offspring[2].strategy.decide(None) == Action.COOP    # Child 2 has mutated
    assert offspring[0].strategy_name == "AlwaysDefect"
    assert offspring[1].strategy_name == "AlwaysCoop"
    assert offspring[2].strategy_name == "AlwaysCoop"
    assert offspring[0].age == 1  # Ensure it has aged
    assert offspring[1].age == 0
    assert offspring[2].age == 0


def test_player_change_strategy(player_coop, player_defect, defect_class, payoff_matrix_3):
    player_coop.change_strategy(defect_class())
    assert player_coop.strategy.decide(None) == Action.DEFECT
    assert player_coop.strategy_name == "AlwaysDefect"
    assert player_coop.age == 0
    assert player_coop.most_recent_score == 0
    # TODO! CHANGE THIS, BECAUSE THE battle METHOD WILL IN THE FUTURE NOT
    # NECESSARILY USE payoff_matrix_3 (the one from config.ini)
    assert player_coop.battle(player_defect, rounds=17) == payoff_matrix_3.as_dict()[(Action.DEFECT, Action.DEFECT)]


def test_flatten():
    list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat_list = flatten(list_of_lists)
    assert flat_list == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_strategy():
    # Make sure it can't be instantiated (an ABC)
    with pytest.raises(TypeError):
        Strategy()

