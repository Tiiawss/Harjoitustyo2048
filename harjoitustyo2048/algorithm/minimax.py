# algorithm/minimax.py
import pygame
import sys
import numpy as np
from base_game.game import Game2048  

def minimax_algorithm(game: Game2048):
    """Looks thru all 4 moves in current game and chooses the one that leads to least amount of tiles on the board.

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
        
        non_zero_tiles = np.count_nonzero(game.matrix)
        
        
        if non_zero_tiles < min_tiles:
            min_tiles = non_zero_tiles
            best_move = direction
        
        
        game.matrix = backup_board

    return best_move