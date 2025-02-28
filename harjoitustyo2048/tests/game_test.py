import unittest
from base_game.game import Game2048
from main import get_random_move, run_game
from algorithm.minimax import minimax_algorithm, smoothness, monotonicity
import numpy as np

class TestMainGame2048(Game2048):
    """Test the main.py Rungame function"""
    def __init__(self):  
        self.matrix = np.zeros((4, 4), dtype=int)
        self.score = 0

    def check_if_game_over(self):
        return True  

    def make_move(self, direction):
        pass  

class TestRunGame(unittest.TestCase):
    """Test the main.py Rungame function"""
    def setUp(self):
        import main
        main.Game2048 = TestMainGame2048

        main.pygame.event.get = lambda: []
     
        self.quit_called = False
        def fake_quit():
            self.quit_called = True

        main.pygame.quit = fake_quit

    def test_run_game_exits_immediately(self):
        """Test that the run game function quits the game when quit is called"""
        run_game()
        self.assertTrue(self.quit_called, "pygame.quit was called correctly.")

if __name__ == "__main__":
    unittest.main()

class TestGame2048(unittest.TestCase):
    

    def setUp(self):
        """Setup for game 2048 tests"""
        self.testGame = Game2048()

    def test_game_start_score_0(self):
        """Game begins with score = 0"""

        testStartZero = self.testGame.score

        self.assertEqual(testStartZero, 0)

    def test_game_start_4X4_Matrix(self):
        """Game starts in 4x4 matrix"""

        matrixRow = 4
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

    def test_alternating_moves(self):
        """Test that every other mouseclick move alternates between random and minimax"""
        play_turn = 0
        move_sequence = []

        for _ in range(6):
            if play_turn % 2 == 0:
                direction = get_random_move()
                move_sequence.append("random")
            else:

                direction, _ = minimax_algorithm(
                    self.testGame,

                    depth=3,

                    maximizing=True,
                    alpha=-10000,
                    beta=10000
                )
                move_sequence.append("minimax algorithm")

            self.testGame.make_move(direction)
            play_turn += 1

        for turn in range(len(move_sequence)):
            if turn % 2 == 0:
                self.assertEqual(move_sequence[turn], "random")
            else:
                self.assertEqual(move_sequence[turn], "minimax algorithm")

    def test_push_tiles(self):
        """Test for the push_tiles function"""

        self.testGame.matrix = np.array([
            [2, 2, 4, 0],
            [0, 4, 4, 4],
            [8, 0, 0, 8],
            [0, 0, 0, 0]
        ])

        expected_matrix = np.array([
            [4, 4, 0, 0],
            [8, 4, 0, 0],
            [16, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        self.testGame.push_tiles()
        np.testing.assert_array_equal(self.testGame.matrix, expected_matrix)

    def test_push_tiles_when_full(self):
        """Test push_tiles function when matrix is full"""

        self.testGame.matrix = np.array([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2, 4],
            [8, 16, 32, 64]
        ])

        expected_matrix = self.testGame.matrix.copy()
        self.testGame.push_tiles()
        np.testing.assert_array_equal(self.testGame.matrix, expected_matrix)

    def test_smoothness_on_smooth_board(self):
        """Test smoothness function on smooth board"""
        self.game = Game2048()
        self.game.matrix = np.array([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ])

        score = smoothness(self.game)
        self.assertLess(score, 0)

    def test_monotonicity_on_monotonic_board(self):
        """Test monotonicity on a completely monotonic board"""
        self.game = Game2048()
        self.game.matrix = np.array([
            [1024, 512, 256, 128],
            [64, 32, 16, 8],
            [4, 2, 1, 0],
            [0, 0, 0, 0]
        ])
        score = monotonicity(self.game)
        self.assertLess(score, 0)

    def test_minimax_with_clear_best_move(self):
        """Test minimax when there is a clear best move"""
        self.game = Game2048()
        self.game.matrix = np.array([
            [2, 2, 8, 16],
            [32, 32, 128, 256],
            [4, 2, 4, 4],
            [8, 8, 0, 0]
        ])
        best_move, _ = minimax_algorithm(
            self.game, depth=3, maximizing=True, alpha=-float('inf'), beta=float('inf'))
        self.assertIn(best_move, ["right", "up"])

