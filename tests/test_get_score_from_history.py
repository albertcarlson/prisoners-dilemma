from tools import History, get_score_from_history, Action



def test_get_score_1():

    history = History(
        own_moves=[
            Action.COOP,
           
        ],
        opponent_moves=[
            Action.COOP,
        ],
    )

    score = get_score_from_history(history)

    assert score == (3, 3), f"Score should be (3, 3), but was {score}. Did you change the payoff matrix?"


def test_get_score_2():

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

    score = get_score_from_history(history)

    assert score == (5, 5), f"Score should be (5, 5), but was {score}. Did you change the payoff matrix?"


def test_get_score_3():

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

    score = get_score_from_history(history)

    assert score == (10, 0), f"Score should be (0, 0), but was {score}. Did you change the payoff matrix?"


def test_get_score_4():

    history = History(
        own_moves=[
            Action.DEFECT,
        ],
        opponent_moves=[
            Action.DEFECT,
        ],
    )

    score = get_score_from_history(history)

    assert score == (1, 1), f"Score should be (1, 1), but was {score}. Did you change the payoff matrix?"


def test_get_score_5():
    
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

    score = get_score_from_history(history)

    assert score == (23, 18), f"Score should be (23, 18), but was {score}. Did you change the payoff matrix?"

