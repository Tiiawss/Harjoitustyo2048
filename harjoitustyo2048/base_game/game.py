import numpy as np
import random


class Game2048:
    """Class where the game logic is stored"""
    
    
    def __init__(self):
        """ The constructor of the class that creates the game
        Returns: The 4x4 game matrix, start score and the beginning situation on board wicth is two tiles
        """
        self.matrix = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        """Adds to a randomized (empty) spot in the game matrix a new tile
        
        returns: either tile with value 2 or 4
        """
        empty_positions = [ 
            (row, col) for row in range(4) for col in range(4) if self.matrix[row][col] == 0
        ]
        if empty_positions:
            row, col = random.choice(empty_positions)
            self.matrix[row][col] = 2 if random.random() < 0.9 else 4

    def push_tiles(self):
        """Move all the tiles to the side towards left in the turned matrix
        
        Returns: matrixs wiht all the tiles pushed as left as possible
        """
        for row in self.matrix:
            contains = row[row != 0]  
            new_row = []
            nothing = False
            for x in range(len(contains)):
                if nothing:
                    nothing = False
                    continue
                
                if x + 1 < len(contains) and contains[x] == contains[x + 1]:
                    new_row.append(contains[x] * 2)
                    self.score += contains[x] * 2
                    nothing = True
                else:
                    new_row.append(contains[x])
            
            new_row.extend([0] * (4 - len(new_row)))
            
            row[:] = new_row

    def turn_matrix(self):
        """Turn the board until all direction changes are the same as sliding the pieces to the left.
        
         Returns: the 2048 matrix turned 90 degrees
        """
        self.matrix = np.rot90(self.matrix, -1)

    def make_move(self, direction):
        """Slide the matrix board pieces to the randomized direction
        
        Args: 
            direction: The direction we are moving the board pieses to from the users pov 
            
        Returns: the game board in the same position it was before and pieces pushed to the direction they were supposed to go
        """
        if direction == "left":
            self.push_tiles()
        elif direction == "right":
            self.turn_matrix()
            self.turn_matrix()
            self.push_tiles()
            self.turn_matrix()
            self.turn_matrix()
        elif direction == "up":
            self.turn_matrix()
            self.turn_matrix()
            self.turn_matrix()
            self.push_tiles()
            self.turn_matrix()
        elif direction == "down":
            self.turn_matrix()
            self.push_tiles()
            self.turn_matrix()
            self.turn_matrix()
            self.turn_matrix()
            
        if 2048 in self.matrix:
            print("Congratulations! You've reached 2048!")

        self.add_new_tile()
        
        

    def check_if_game_over(self):
        """Checks if there is either tile 2048 reached or no more spaces left
       
        returns: True if game over, false otherwise
        """
        if 2048 in self.matrix:
            return True 
        if np.any(self.matrix == 0):  
            return False
        for direction in ["left", "right", "up", "down"]:
            backup_board = self.matrix.copy()
            self.make_move(direction)
            if not np.array_equal(self.matrix, backup_board):
                self.matrix = backup_board
                return False
        return True

    def get_game(self):
        """Print the current game state.
       
        Returns: Current game
        """
        print(self.matrix)
