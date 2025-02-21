import numpy as np
import copy
from base_game.game import Game2048


def smoothness(game: Game2048):
    """
      Rates the smoothness of the matrix

    Args:
        The game board

    returns:
    Score for the smoothness
    """
    smooth_score = 0
    for row in range(4):
        for col in range(4):
            if game.matrix[row][col] != 0:
                value = np.log2(game.matrix[row][col])

                if col < 3 and game.matrix[row][col + 1] != 0:
                    neighbor_value = np.log2(game.matrix[row][col + 1])
                    smooth_score -= abs(value - neighbor_value)

                if row < 3 and game.matrix[row + 1][col] != 0:
                    neighbor_value = np.log2(game.matrix[row + 1][col])
                    smooth_score -= abs(value - neighbor_value)
    return smooth_score


def monotonicity(game: Game2048):
    """
    Rates the monocity of the matrix

    Args:
        The game board

    returns:
    Score for the monoticity
    """
    mono_score = 0

    for row in range(4):
        for col in range(3):
            if game.matrix[row][col] and game.matrix[row][col + 1]:
                mono_score -= abs(np.log2(game.matrix[row][col]) -
                                  np.log2(game.matrix[row][col + 1]))

    for col in range(4):
        for row in range(3):
            if game.matrix[row][col] and game.matrix[row + 1][col]:
                mono_score -= abs(np.log2(game.matrix[row][col]) -
                                  np.log2(game.matrix[row + 1][col]))
    return mono_score


def board_sitsuation(game: Game2048):
    """Check the board state and count Weighted snake matrix and smhoothness and monotonisity"""

    weights = np.array([
        [2**15, 2**14, 2**13, 2**12],
        [2**8, 2**9, 2**10, 2**11],
        [2**7, 2**6, 2**5, 2**4],
        [2**0, 2**1, 2**2, 2**3]
    ])

    weighted_sum = np.sum(game.matrix * weights)

    smoothnes_x = 18.0
    smoothness_weight = smoothnes_x * smoothness(game)

    monotonicity_x = 10.0
    mono_weight = monotonicity_x * monotonicity(game)

    return weighted_sum + smoothness_weight + mono_weight


def emptyes(game: Game2048):
    """Returns a tuple list of empty tiles in the matrix."""
    empty_spots = []
    for row in range(4):
        for col in range(4):
            if game.matrix[row][col] == 0:
                empty_spots.append((row, col))
    return empty_spots


def minimax_algorithm(
        game: Game2048,
        depth: int,
        max_depth: int,
        maximizing: bool,
        alpha: float,
        beta: float):
    """Looks thru all 4 moves in current game and chooses the one that leads to
            least amount of tiles on the board.

    Args:
        game (Game2048): The current game state.
        depth: how deep in the minmax tree the algorithm looks
        Maximizing: Boolean on whos turn is it, the maximazer on minimizer
        alpha: the aplha beta prunings alpha, maximizer best optin thus far
        beta: the aplha beta prunings alpha, minimizer best optin thus far

    Returns:
        str: The "optimal" direction out of the four ('left', 'right', 'up', 'down').
    """

    if depth == 0:
        return None, board_sitsuation(game)

    tile_sum = np.count_nonzero(game.matrix)
    if tile_sum == 16:

        return None, -10000 + (max_depth - depth)

    directions = ["left", "right", "up", "down"]
    best_move = None

    if maximizing:
        max_eval = -10000000
        possibilities = []
        valid_move_found = False

        for direction in directions:
            backup_game = copy.deepcopy(game)
            game.make_move(direction)
            if np.array_equal(game.matrix, backup_game.matrix):
                game = backup_game
                continue
            valid_move_found = True
            heuristic_score = board_sitsuation(game)
            possibilities.append(
                (direction, copy.deepcopy(game), heuristic_score))
            game = backup_game

        if not valid_move_found:

            return None, board_sitsuation(game)

        possibilities.sort(key=lambda x: x[2], reverse=True)

        for direction, state, _ in possibilities:
            backup_game = copy.deepcopy(game)
            game = state
            _, eval_score = minimax_algorithm(
                game, depth - 1, max_depth, False, alpha, beta)
            game = backup_game
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = direction
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        if best_move is None and possibilities:
            best_move = possibilities[0][0]
            max_eval = possibilities[0][2]

        return best_move, max_eval

    else:

        min_eval = 1000000
        empty_positions = emptyes(game)
        if not empty_positions:
            return None, board_sitsuation(game)
        for value in [2, 4]:
            for row, col in empty_positions:
                backup_game = copy.deepcopy(game)
                game.matrix[row][col] = value
                _, eval_score = minimax_algorithm(
                    game, depth - 1, max_depth, True, alpha, beta)
                game = backup_game
                if eval_score < min_eval:
                    min_eval = eval_score
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return None, min_eval



