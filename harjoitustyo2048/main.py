# main.py

import sys
import random
from base_game.game import Game2048
from ui.visual import make_the_matrix
from algorithm.minimax import minimax_algorithm
import pygame
import numpy as np


def get_random_move():
    """Makes a randomized move to any of four direction in the game

    Returns: direction
    """
    return random.choice(["left", "right", "up", "down"])


def run_game():
    """Starts and runs the 2048 game loop,
     writes in console what moves are being made
     """
    current_game = Game2048()
    play_turn = 0

    while not current_game.check_if_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_turn % 2 == 0:
                    direction = get_random_move()
                    print(f"Random move: {direction}")
                    current_game.make_move(direction)
                    play_turn += 1
                else:
                    tile_count = np.count_nonzero(current_game.matrix)

                    if tile_count >= 16:
                        depth = 11
                        max_depth = 7
                    elif tile_count >= 8:
                        depth = 5
                        max_depth = 5
                    else:
                        depth = 3
                        max_depth = 3

                    direction, eval_score = minimax_algorithm(
                        current_game, depth=depth, max_depth=max_depth,
                        maximizing=True, alpha=-1000000, beta=1000000
                    )
                    print(f"Minimax move: ({direction}, {eval_score})")
                    current_game.make_move(direction)
                    play_turn += 1

        make_the_matrix(current_game)
        pygame.display.flip()

    max_tile = current_game.matrix.max()
    print("Game Over!")
    print("Max tile was:", max_tile)
    pygame.quit()


if __name__ == "__main__":
    """ beginning of the game"""
    run_game()
