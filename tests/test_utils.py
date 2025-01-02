from utils import History, Action, PayoffMatrix
import pytest


@pytest.fixture
def payoff_matrix():
    return PayoffMatrix.from_config("config.ini")


def test_get_score_1(payoff_matrix):

    history = History(
        own_moves=[
            Action.COOP,
           
        ],
        opponent_moves=[
            Action.COOP,
        ],
    )

    score = history.get_score()

    assert score == payoff_matrix.get_reward(Action.COOP, Action.COOP), f"Score should be (3, 3), but was {score}."


def test_get_score_2(payoff_matrix):

    history = History(
        own_moves=[
            Action.COOP,
            Action.DEFECT,
        ],
        opponent_moves=[
            Action.DEFECT,
            Action.COOP,
        ],
    )

    score = history.get_score()

    expected_score = (payoff_matrix.get_reward(Action.COOP, Action.DEFECT)[0] + payoff_matrix.get_reward(Action.DEFECT, Action.COOP)[0]) / 2

    assert score == (expected_score, expected_score), f"Score should be ({expected_score}, {expected_score}), but was {score}."


def test_get_score_3(payoff_matrix):

    history = History(
        own_moves=[
            Action.DEFECT,
            Action.DEFECT,
        ],
        opponent_moves=[
            Action.COOP,
            Action.COOP,
        ],
    )

    score = history.get_score()

    expected_a, expected_b = payoff_matrix.get_reward(Action.DEFECT, Action.COOP)

    assert score == (expected_a, expected_b), f"Score should be ({expected_a}, {expected_b}), but was {score}."


def test_get_score_4(payoff_matrix):

    history = History(
        own_moves=[
            Action.DEFECT,
        ],
        opponent_moves=[
            Action.DEFECT,
        ],
    )

    score = history.get_score()
    expected_score = payoff_matrix.get_reward(Action.DEFECT, Action.DEFECT)

    assert score == expected_score, f"Score should be {expected_score}, but was {score}. Did you change the payoff matrix?"


def test_get_score_5(payoff_matrix):
    
    history = History(
        own_moves=[
            Action.COOP,
            Action.DEFECT,
            Action.COOP,
            Action.COOP,
            Action.COOP,
            Action.DEFECT,
            Action.DEFECT,
            Action.DEFECT,
            Action.DEFECT,
        ],
        opponent_moves=[
            Action.COOP,
            Action.COOP,
            Action.COOP,
            Action.DEFECT,
            Action.DEFECT,
            Action.COOP,
            Action.DEFECT,
            Action.DEFECT,
            Action.COOP,
        ],
    )

    score = history.get_score()

    expected_a = 2 * payoff_matrix.get_reward(Action.COOP, Action.COOP)[0] \
               + 2 * payoff_matrix.get_reward(Action.COOP, Action.DEFECT)[0] \
               + 3 * payoff_matrix.get_reward(Action.DEFECT, Action.COOP)[0] \
               + 2 * payoff_matrix.get_reward(Action.DEFECT, Action.DEFECT)[0]
    
    expected_b = 2 * payoff_matrix.get_reward(Action.COOP, Action.COOP)[1] \
               + 2 * payoff_matrix.get_reward(Action.COOP, Action.DEFECT)[1] \
               + 3 * payoff_matrix.get_reward(Action.DEFECT, Action.COOP)[1] \
               + 2 * payoff_matrix.get_reward(Action.DEFECT, Action.DEFECT)[1]
    
    expected_a /= len(history)
    expected_b /= len(history)

    assert score == (expected_a, expected_b), f"Score should be ({expected_a}, {expected_b}), but was {score}."

