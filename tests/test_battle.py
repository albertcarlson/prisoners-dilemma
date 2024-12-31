from utils import Player, Action, battle, PayoffMatrix
from catalogue import EXAMPLE_SPECIES
import pytest


@pytest.fixture
def payoff_matrix():
    return PayoffMatrix.from_config("config.ini")


def test_tit_for_tat_battle(payoff_matrix):

    tit4tat1 = Player(EXAMPLE_SPECIES["TitForTat"])
    tit4tat2 = Player(EXAMPLE_SPECIES["TitForTat"])

    score = battle(tit4tat1, tit4tat2, rounds=100)

    # TODO! CHANGE THIS, BECAUSE THE battle METHOD WILL IN THE FUTURE NOT
    # NECESSARILY USE payoff_matrix_3 (the one from config.ini)
    coop_coop_1, coop_coop_2 = payoff_matrix.get_reward(Action.COOP, Action.COOP)

    expected_score = (1.0*coop_coop_1, 1.0*coop_coop_2)

    assert score == expected_score, f"Unexpectedly, the score wasn't {expected_score} but instead {score} when battling two tit for tats...?"


def test_tit_for_tat_vs_tester(payoff_matrix):

    tit4tat = Player(EXAMPLE_SPECIES["TitForTat"])
    tester  = Player(EXAMPLE_SPECIES["Tester"])

    score = battle(tit4tat, tester, rounds=100)

    # TODO! CHANGE THIS, BECAUSE THE battle METHOD WILL IN THE FUTURE NOT
    # NECESSARILY USE payoff_matrix_3 (the one from config.ini)
    coop_coop_1, coop_coop_2     = payoff_matrix.get_reward(Action.COOP, Action.COOP)
    coop_defect_1, coop_defect_2 = payoff_matrix.get_reward(Action.COOP, Action.DEFECT)
    defect_coop_1, defect_coop_2 = payoff_matrix.get_reward(Action.DEFECT, Action.COOP)

    expected_score = ((98*coop_coop_1+coop_defect_1+defect_coop_1) / 100, (98*coop_coop_2 + coop_defect_2 + defect_coop_2) / 100)

    assert score == expected_score, f"Unexpectedly, the score wasn't {expected_score} but instead {score} when battling tit for tat vs tester...?"
