from utils import Strategy, Action, History, PAYOFF_MATRIX#, Player, <--- TODO! test Player class
from collections.abc import MutableSequence
import pytest


def test_payoff_matrix():
    # make sure all 4 action combinations are in the payoff matrix
    assert len(PAYOFF_MATRIX) == 4
    assert (Action.COOP, Action.COOP) in PAYOFF_MATRIX, f"Didn't find COOP, COOP in payoff matrix"
    assert (Action.COOP, Action.DEFECT) in PAYOFF_MATRIX, f"Didn't find COOP, DEFECT in payoff matrix"
    assert (Action.DEFECT, Action.COOP) in PAYOFF_MATRIX, f"Didn't find DEFECT, COOP in payoff matrix"
    assert (Action.DEFECT, Action.DEFECT) in PAYOFF_MATRIX, f"Didn't find DEFECT, DEFECT in payoff matrix"
    # assert types are correct
    assert isinstance(PAYOFF_MATRIX, dict), f"PAYOFF_MATRIX should be a dict, but was {type(PAYOFF_MATRIX)}"
    assert isinstance(PAYOFF_MATRIX[(Action.COOP, Action.COOP)], tuple), f"PAYOFF_MATRIX[(Action.COOP, Action.COOP)] should be a tuple, but was {type(PAYOFF_MATRIX[(Action.COOP, Action.COOP)])}"
    assert isinstance(PAYOFF_MATRIX[(Action.COOP, Action.DEFECT)], tuple), f"PAYOFF_MATRIX[(Action.COOP, Action.DEFECT)] should be a tuple, but was {type(PAYOFF_MATRIX[(Action.COOP, Action.DEFECT)])}"
    assert isinstance(PAYOFF_MATRIX[(Action.DEFECT, Action.COOP)], tuple), f"PAYOFF_MATRIX[(Action.DEFECT, Action.COOP)] should be a tuple, but was {type(PAYOFF_MATRIX[(Action.DEFECT, Action.COOP)])}"
    assert isinstance(PAYOFF_MATRIX[(Action.DEFECT, Action.DEFECT)], tuple), f"PAYOFF_MATRIX[(Action.DEFECT, Action.DEFECT)] should be a tuple, but was {type(PAYOFF_MATRIX[(Action.DEFECT, Action.DEFECT)])}"
    # assert length of tuples is correct
    assert len(PAYOFF_MATRIX[(Action.COOP, Action.COOP)]) == 2, f"PAYOFF_MATRIX[(Action.COOP, Action.COOP)] should be a tuple of length 2, but was {len(PAYOFF_MATRIX[(Action.COOP, Action.COOP)])}"
    assert len(PAYOFF_MATRIX[(Action.COOP, Action.DEFECT)]) == 2, f"PAYOFF_MATRIX[(Action.COOP, Action.DEFECT)] should be a tuple of length 2, but was {len(PAYOFF_MATRIX[(Action.COOP, Action.DEFECT)])}"
    assert len(PAYOFF_MATRIX[(Action.DEFECT, Action.COOP)]) == 2, f"PAYOFF_MATRIX[(Action.DEFECT, Action.COOP)] should be a tuple of length 2, but was {len(PAYOFF_MATRIX[(Action.DEFECT, Action.COOP)])}"
    assert len(PAYOFF_MATRIX[(Action.DEFECT, Action.DEFECT)]) == 2, f"PAYOFF_MATRIX[(Action.DEFECT, Action.DEFECT)] should be a tuple of length 2, but was {len(PAYOFF_MATRIX[(Action.DEFECT, Action.DEFECT)])}"


def test_action():
    # make sure the enum has exactly 2 values, COOP and DEFECT
    assert len(Action) == 2, f"Action should have exactly 2 values, but had {len(Action)}"
    assert Action.COOP in Action, f"Action.COOP should be in Action, but wasn't"
    assert Action.DEFECT in Action, f"Action.DEFECT should be in Action, but wasn't"


def test_history():
    history = History()

    # make sure the two fields are called own_moves and opponent_moves
    assert hasattr(history, "own_moves"), f"history should have a field called own_moves, but didn't"
    assert hasattr(history, "opponent_moves"), f"history should have a field called opponent_moves, but didn't"
    # make sure they are lists
    assert isinstance(history.own_moves, MutableSequence), f"history.own_moves should be a list, but was {type(history.own_moves)}"
    assert isinstance(history.opponent_moves, MutableSequence), f"history.opponent_moves should be a list, but was {type(history.opponent_moves)}"
    
    # test the 7 methods append,len,iter,invert,score,repr,str
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
    # (tested in another file)

    # __repr__
    expected = "History(own_moves=[<Action.DEFECT: True>], opponent_moves=[<Action.COOP: False>])"
    assert repr(history) == expected, f"History.__repr__ should be '{expected}', but was {repr(history)}"

    # __str__
    # (omitted)


def test_strategy():
    # make sure it can't be instantiated (an ABC)
    with pytest.raises(TypeError):
        Strategy()

