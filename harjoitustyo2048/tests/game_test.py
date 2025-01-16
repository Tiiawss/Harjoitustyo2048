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

