import unittest
from base_game.game import Game2048  


class TestGame2048(unittest.TestCase):  
    def setUp(self):
        """Setup game 2048 for tests"""
        self.testGame = Game2048()  

    def test_game_start_score_0(self):
        """Game begins with score = 0"""
        
        testStartZero = self.testGame.score
        
        self.assertEqual(testStartZero, 0)
        
    def test_game_start_4X4_Matrix(self):
        """Game starts in 4x4 matrix"""

        matrixRow  = 4
        matrixColumn = 4
        matrix = self.testGame.matrix
        self.assertEqual(len(matrix), matrixRow)
        for row in matrix:
            self.assertEqual(len(row), matrixColumn)
            
    def test_game_setUp_two_tiles(self):
        """Test that the game starts with two tiles placed on the board"""
    
        matrix = self.testGame.matrix
        not_zero_tiles = 0
        for row in matrix:
            not_zero_tiles += sum(1 for cell in row if cell != 0)
        self.assertEqual(not_zero_tiles, 2)
        

        
        
          
            
        


