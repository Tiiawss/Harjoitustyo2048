import numpy as np
import copy
from base_game.game import Game2048


def smoothness(game: Game2048):
    """
    Rates the smoothness of the matrix, i.e. how the numbers increase or decrease throughout the matrix.

    Args:
        game (Game2048): The game board.

    Returns:
        float: The smoothness score.
    """
    board_smoothness = 0
    for row in range(4):
        for col in range(4):
            current_tile = game.matrix[row][col]
            if current_tile != 0:
                if col < 3 and game.matrix[row][col + 1] != 0:
                    previous_tile = game.matrix[row][col + 1]
                    board_smoothness -= abs(current_tile - previous_tile) / max(current_tile, previous_tile)
                if row < 3 and game.matrix[row + 1][col] != 0:
                    previous_tile = game.matrix[row + 1][col]
                    board_smoothness -= abs(current_tile - previous_tile) / max(current_tile, previous_tile)
    return board_smoothness


def monotonicity(game: Game2048):
    """
    Rates the monotonicity of the matrix.

    Args:
        game (Game2048): The game board.

    Returns:
        float: The monotonicity score.
    """
    board_monotonicity = 0
    for row in range(4):
        for col in range(3):
            current_tile = game.matrix[row][col]
            next_tile = game.matrix[row][col + 1]
            if current_tile and next_tile:
                board_monotonicity -= abs(current_tile - next_tile) / max(current_tile, next_tile)
    for col in range(4):
        for row in range(3):
            current_tile = game.matrix[row][col]
            next_tile = game.matrix[row + 1][col]
            if current_tile and next_tile:
                board_monotonicity -= abs(current_tile - next_tile) / max(current_tile, next_tile)
    return board_monotonicity


def board_situation(game: Game2048):
    """
    Checks the board state and calculates a weighted sum that includes smoothness and monotonicity.

    Args:
        game (Game2048): The game board.

    Returns:
        float: The evaluated board situation.
    """
    weights = np.array([
        [2**15, 2**14, 2**13, 2**12],
        [2**8, 2**9, 2**10, 2**11],
        [2**7, 2**6, 2**5, 2**4],
        [2**0, 2**1, 2**2, 2**3]
    ])
    weighted_sum = np.sum(game.matrix * weights)
    smoothness_x = 18.0
    smoothness_weight = smoothness_x * smoothness(game)
    monotonicity_x = 10.0
    mono_weight = monotonicity_x * monotonicity(game)
    return weighted_sum + smoothness_weight + mono_weight


def empties(game: Game2048):
    """
    Returns a list of tuples representing empty tiles in the matrix.

    Args:
        game (Game2048): The game board.

    Returns:
        List[Tuple[int, int]]: The list of empty positions.
    """
    empty_spots = []
    for row in range(4):
        for col in range(4):
            if game.matrix[row][col] == 0:
                empty_spots.append((row, col))
    return empty_spots


def print_board_info(game: Game2048, label=""):
    """
    Prints the board state and the individual heuristic components:
    weighted_sum, smoothness_weight, and mono_weight.
    """
    weights = np.array([
        [2**15, 2**14, 2**13, 2**12],
        [2**8, 2**9, 2**10, 2**11],
        [2**7, 2**6, 2**5, 2**4],
        [2**0, 2**1, 2**2, 2**3]
    ])
    weighted_sum = np.sum(game.matrix * weights)
    smoothness_x = 18.0
    s = smoothness(game)
    smoothness_weight = smoothness_x * s
    monotonicity_x = 10.0
    m = monotonicity(game)
    mono_weight = monotonicity_x * m

    print(f"{label} Board state:")
    for row in game.matrix:
        print(row)
    print(f"weighted_sum: {weighted_sum}, smoothness_weight: {smoothness_weight}, mono_weight: {mono_weight}\n")


def minimax_algorithm(game: Game2048, depth: int, maximizing: bool, alpha: float, beta: float):
    """
    Uses minimax with alpha-beta pruning to determine the best move.

    Args:
        game (Game2048): The current game state.
        depth (int): Current depth in the minimax tree.
        maximizing (bool): True if it's the maximizing player's turn.
        alpha (float): Alpha-beta pruning - best maximizer score.
        beta (float): Alpha-beta pruning - best minimizer score.

    Returns:
        Tuple[Optional[str], float]: The optimal move and its evaluation score.
    """
    directions = ["left", "right", "up", "down"]

    if maximizing:
        best_move = None
        max_eval = -1000000
        possibilities = []

        for direction in directions:
            new_game = Game2048()
            new_game.matrix = game.matrix.copy()
            new_game.make_move(direction)

            if np.array_equal(game.matrix, new_game.matrix):
                continue

           
            print_board_info(new_game, f"Maximizing move: {direction}")

            h_score = board_situation(new_game)
            possibilities.append((direction, new_game, h_score))

        if not possibilities:
            return None, board_situation(game)

        possibilities.sort(key=lambda x: x[2], reverse=True)

        for direction, state, _ in possibilities:
            _, eval_score = minimax_algorithm(state, depth - 1, False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = direction
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break 
        return best_move, max_eval

    else:
        if depth == 0 or np.count_nonzero(game.matrix) == 16:
            return None, board_situation(game)

        min_eval = 1000000
        empty_positions = empties(game)
        if not empty_positions:
            return -depth, board_situation(game)

        for row, col in empty_positions:
            for value in [4, 2]:
                new_game = Game2048()
                new_game.matrix = game.matrix.copy()
                new_game.matrix[row][col] = value

                
                print_board_info(new_game, f"Minimizing: placed {value} at ({row}, {col})")

                _, eval_score = minimax_algorithm(new_game, depth - 1, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                beta = min(beta, eval_score)
                if beta <= alpha:
                    return None, min_eval
        
        return None, min_eval
