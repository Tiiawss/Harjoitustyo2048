# algorithm/minimax.py
import numpy as np
from base_game.game import Game2048


def board_sitsuation(game: Game2048):
    """Check the board state."""
    return np.count_nonzero(game.matrix)

def emptyes(game: Game2048):
    """Returns a tuple list of empty tiles in the matrix."""
    
    empty_spots = []
    
    for row in range(4):
        for col in range(4):
            if game.matrix[row][col] == 0:
                empty_spots.append((row, col))
    
    return empty_spots
    
    

def minimax_algorithm(game: Game2048, depth: int, maximizing: bool):
    """Looks thru all 4 moves in current game and chooses the one that leads to 
            least amount of tiles on the board.

    Args:
        game (Game2048): The current game state.
        depth: how deep in the minmax tree the algorithm looks
        Maximizing: Boolean on whos turn is it, the maximazer on minimizer

    Returns:
        str: The "optimal" direction out of the four ('left', 'right', 'up', 'down').
    """
   
    tile_sum = board_sitsuation(game)
    if tile_sum == 16:  
        return None, 0
    if depth == 0:
        return None, tile_sum

    directions = ["left", "right", "up", "down"]
    best_move = None
    
    if maximizing:
        max_eval = -1000000
        for direction in directions:
            backup_board = game.matrix.copy()
            game.make_move(direction)
            _, eval_score = minimax_algorithm(game, depth - 1, False)
            game.matrix = backup_board
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = direction
        return best_move, max_eval
    else:
        
        min_eval = 1000000
        empty_positions = emptyes(game)
        
        best_move_min = []
        
        for value in [4, 2]:  
            for row, col in empty_positions:  
                backup_board = game.matrix.copy()
                game.matrix[row][col] = value  
                
                _, eval_score = minimax_algorithm(game, depth - 1, True)
                
                game.matrix = backup_board  
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move_min = [(row, col, value)]
                elif eval_score == min_eval:
                    best_move_min.append((row, col, value))
                    
            else:
                break  
        
        return best_move_min, min_eval


