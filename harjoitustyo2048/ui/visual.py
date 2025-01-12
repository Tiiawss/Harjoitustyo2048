# ui/visual.py
import pygame
import sys
from base_game.game import Game2048  
import random

font_size = 34
width, height = 500, 500
grid_size = 4
cell_size = width // grid_size
background_color = (188, 173, 161)
text_color = (119, 114, 102)
cell_color = (206, 194, 179)


pygame.init()


ui = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")
font = pygame.font.SysFont("Arial", font_size)


def make_the_matrix(game):
    """Makes the games visual side, shows the 4x4 matrix and the tiles to the user
    
    Args: Takes the game it shows as argument"""
   
    ui.fill(background_color)

    for row in range(4):
        for colum in range(4):
            tile_value = game.matrix[row][colum]
            rect = pygame.Rect(colum * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(ui, cell_color, rect)

            if tile_value != 0:
                text = font.render(str(tile_value), True, text_color)
                text_rect = text.get_rect(center=rect.center)
                ui.blit(text, text_rect)

    pygame.display.update()

