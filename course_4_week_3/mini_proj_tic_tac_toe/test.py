 if player == provided.PLAYERX:
        best_move = ()
        best_score = -1
        for square in empty_squares:
            clone_board = board.clone()
            clone_board.move(square[0], square[1], player)
            non_player = (square[0], square[1])
            score, move = mm_move(clone_board, provided.PLAYERO)
            if score > best_score:
                best_score = score
                best_move = non_player
            if score == SCORES[player]:
                return score, non_player
        return best_score, best_move
    if player == provided.PLAYERO:
        best_move = ()
        best_score = 1
        for square in empty_squares:
            clone_board = board.clone()
            clone_board.move(square[0], square[1], player)
            non_player = (square[0], square[1])
            score, move = mm_move(clone_board, provided.PLAYERX)
            if score < best_score:
                best_score = score
                best_move = non_player
            if score == SCORES[player]:
                return score, non_player
        return best_score, best_move
