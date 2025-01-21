# main.py

from base_game.game import Game2048
from ui.visual import make_the_matrix
import pygame
import sys
import random

def get_random_move():
    """Makes a randomized move to any of four direction in the game
    
    Returns: direction
    """
    return random.choice(["left", "right", "up", "down"])


def run_game():
    """Starts and keeps the 2048 game going the game loop, writes in console what moves are being made
    
    """
    current_game = Game2048()

    while not current_game.check_if_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                direction = get_random_move()
                print(f"Random move: {direction}")
                current_game.make_move(direction)
                

        make_the_matrix(current_game)
        
        pygame.display.flip()

    print("Game Over!")
    pygame.quit()


if __name__ == "__main__":
    """ beginning of the game"""
    run_game()
