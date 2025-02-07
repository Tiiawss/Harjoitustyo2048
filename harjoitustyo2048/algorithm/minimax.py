# algorithm/minimax.py
import numpy as np
from base_game.game import Game2048


def board_sitsuation(game: Game2048):
    """Check the board state."""
    return np.count_nonzero(game.matrix)



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
    """tähän tarkistus jos täysi  kutsu board stistua, muuttuja talteen, jos nolla palauta nolla, muuten minimaxiin  
    
    - kuinka syvällä menee täyteen(nyt turha), ota pois float inf, korvaa vaikka 100000 ja -1000000"""
    if depth == 0 :
        return None, board_sitsuation(game)

    directions = ["left", "right", "up", "down"]
    best_move = None
    
    if maximizing:
        max_eval = float('-inf')
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
        """vapaiden ruutujen lista, ota funkkarista talteen lista vapaita siirtoja, -> se käy läpi arvot 4,2 esim. kaks siäistä silmukkaa ulommassa arvot 4 ja 2 ja sisemmässä sijainnit
        minimoija sijoittaa laudalle numerot 
        voi tarkistaa onko lauta täynnä niin että mikään siirto ei ole mahdollista samalla funkkarilla mikä latsoo mahdolliset siirrot koska jos se palauttaa nolla mahdollisuutta.
        
        tarvii minimaxin aikana olla tulematta game lokiikasta, vaan oma minimaxin aikana, (ei make move) 
        
        katso miten pythonista hypärään kerralla kahdesta silmukasta ulos, palauta tuple lista joka palauttaa 
        """
        min_eval = float('inf')
        for direction in directions:
            backup_board = game.matrix.copy()
            game.make_move(direction)
            _, eval_score = minimax_algorithm(game, depth - 1, True)
            game.matrix = backup_board
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = direction
        return best_move, min_eval


