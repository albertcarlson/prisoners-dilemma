from utils import History, Action



def test_get_score_1():

    history = History(
        own_moves=[
            Action.COOP,
           
        ],
        opponent_moves=[
            Action.COOP,
        ],
    )

    score = history.score

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

    score = history.score

    assert score == (2.5, 2.5), f"Score should be (2.5, 2.5), but was {score}. Did you change the payoff matrix?"


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

    score = history.score

    assert score == (5.0, 0.0), f"Score should be (5.0, 0.0), but was {score}. Did you change the payoff matrix?"


def test_get_score_4():

    history = History(
        own_moves=[
            Action.DEFECT,
        ],
        opponent_moves=[
            Action.DEFECT,
        ],
    )

    score = history.score

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

    score = history.score

    assert score == (2.5555555555555554, 2.0), f"Score should be (23, 18), but was {score}. Did you change the payoff matrix?"


# def test_print_history():
    
#     history = History(
#         own_moves=[
#             Action.COOP,
#             Action.DEFECT,
#             Action.COOP,
#             Action.COOP,
#             Action.COOP,
#             Action.DEFECT,
#             Action.DEFECT,
#             Action.DEFECT,
#             Action.DEFECT,
#         ],
#         opponent_moves=[
#             Action.COOP,
#             Action.COOP,
#             Action.COOP,
#             Action.DEFECT,
#             Action.DEFECT,
#             Action.COOP,
#             Action.DEFECT,
#             Action.DEFECT,
#             Action.COOP,
#         ],
#     )
    
#     print(history)
#     # assert input("Does the above look alright? [y/n] ").lower() in ("y", "yes"), "The printed history does not look as expected."
#     assert False, "not properly implemented yet..."
