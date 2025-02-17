import random
import pygame
from unittest import *
from game_board import Board
from dice import Dice

pygame.init()


# Tests Board Generation
class TestGameBoard(TestCase):

    def test_Board_invalid_height_width(self):
        self.assertRaises(TypeError, Board, "str", "str")
        self.assertRaises(TypeError, Board, 10, "str")
        self.assertRaises(TypeError, Board, "str", 10)

    def test_Board_Layouts(self):

        # Initialise Board with seed
        random.seed(27)
        board = Board(1, 1)

        # Test the Default Board Generation
        self.assertEqual(board.tile_list, ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                     "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                    ])
        self.assertEqual(board.numbers, [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11])

        # Shuffles Board
        board.shuffle_board()

        # Test Shuffled Board
        self.assertEqual(board.tile_list, ['B', 'Wo', 'O', 'Wh', 'O', 'Wh', 'O', 'S', 'Wo', 'Wo', 'S', 'Wh', 'B',
                                           'Wh', 'S', 'B', 'D', 'Wo', 'S'])
        self.assertEqual(board.numbers, [12, 8, 3, 5, 10, 3, 11, 9, 6, 6, 5, 10, 4, 9, 8, 2, 11, 4])

        # Sets Beginner Board
        board.beginner_board()

        # Test Beginner Board is Correct
        self.assertEqual(board.tile_list, ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                                           "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                                           ])
        self.assertEqual(board.numbers, [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11])


# Tests Dice Rolling
class TestDice(TestCase):

    def test_Dice_invalid_height_width(self):
        self.assertRaises(TypeError, Dice, "str", "str")
        self.assertRaises(TypeError, Dice, 10, "str")
        self.assertRaises(TypeError, Dice, "str", 10)

    def test_Dice_init_Value(self):
        random.seed(27)
        dice = Dice(1, 1)
        self.assertEqual(dice.values, [6, 4])
        self.assertEqual(dice.result, 10)

    def test_Dice_roll_dice(self):
        random.seed(27)
        dice = Dice(1, 1)
        dice.roll_dice()
        self.assertEqual(dice.values, [6, 3])
        self.assertEqual(dice.result, 9)


# Test functions that require the combination of other functions
class TestMain(TestCase):

    def setUp(self):
        random.seed(27)

        # Screen Size
        SCREENWIDTH = 1000
        SCREENHEIGHT = SCREENWIDTH * .80  # 800 pixels

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Catan")
        self.dice_vals = Dice(SCREENWIDTH, SCREENHEIGHT)

        self.board = Board(SCREENWIDTH, SCREENHEIGHT)

    def draw(self):
        self.board.draw_board(self.screen, self.dice_vals.result)

    # Test if robber pos is changed properly
    def test_robber_pos(self):
        self.draw()

        # Checks if Robber is in the Default Pos
        self.assertEqual(self.board.robber_pos, (500.0, 383.33333333333337))

        # Shuffles Board
        self.board.shuffle_board()
        self.draw()

        # Checks if Robber is in new Pos
        self.assertEqual(self.board.robber_pos, (500.0, 633.3333333333334))

        # Sets board to beginner
        self.board.beginner_board()
        self.draw()

        # Checks if Robber is in the default pos
        self.assertEqual(self.board.robber_pos, (500.0, 383.33333333333337))

    # Tests if the values of the tile list, and number list are changed after board is drawn
    def test_value_changes_board(self):
        self.setUp()
        self.draw()


        self.assertEqual(self.board.tile_list, ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                                           "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                                           ])
        self.assertEqual(self.board.numbers, [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11])








