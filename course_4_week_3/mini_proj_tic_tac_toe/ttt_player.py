"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    # empty_squares = board.get_empty_squares()

    winner = board.check_win()
    move = ()
    score = 0

    if winner != None:

        move = (-1, -1)

        return SCORES[winner], move

    empty_squares = board.get_empty_squares()

    best_move = ()
    best_score = SCORES[player]
    for square in empty_squares:
        clone_board = board.clone()
        clone_board.move(square[0], square[1], player)
        non_player = (square[0], square[1])
        score, move = mm_move(clone_board, provided.switch_player(player))

        if score > best_score:
            best_score = score
            best_move = non_player
        if score == SCORES[player]:
            return score, non_player
    return best_score, best_move


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
