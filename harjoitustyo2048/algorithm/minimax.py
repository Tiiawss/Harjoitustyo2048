# algorithm/minimax.py
import numpy as np
from base_game.game import Game2048


def board_sitsuation(game: Game2048):
    """Check the board state."""
    return np.count_nonzero(game.matrix)



def minimax_algorithm(game: Game2048):
    """Looks thru all 4 moves in current game and chooses the one that leads to 
            least amount of tiles on the board.

    Args:
        game (Game2048): The current game state.

    Returns:
        str: The "optimal" direction out of the four ('left', 'right', 'up', 'down').
    """
    directions = ["left", "right", "up", "down"]
    best_move = None
    min_tiles = float('inf')

    for direction in directions:

        backup_board = game.matrix.copy()

        game.make_move(direction)

        non_zero_tiles = board_sitsuation(game)
        
        print(f"Move: {direction}")
        
        print(f"Empty tiles after move: {non_zero_tiles}")
        

        if non_zero_tiles < min_tiles:
            min_tiles = non_zero_tiles
            best_move = direction

        game.matrix = backup_board

    print (f"Best move: {best_move}")
    return best_move
