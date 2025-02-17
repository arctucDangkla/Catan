import random
import pygame
from unittest import *
from unittest.mock import MagicMock
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

    def test_initialization(self):
        random.seed(27)
        width = 1
        height = 1
        dice = Dice(width, height)

        self.assertEqual(len(dice.values), 2)
        self.assertTrue(1 <= dice.values[0] <= 6)
        self.assertTrue(1 <= dice.values[1] <= 6)
        self.assertEqual(dice.result, sum(dice.values))
        self.assertEqual(dice.size, 60)
        self.assertEqual(dice.spacing, 20)
        self.assertEqual(dice.total_width, 140)
        self.assertEqual(dice.x, (width - dice.total_width) // 2)
        self.assertEqual(dice.y, height - 80)

    def test_roll_dice(self):
        dice = Dice(1, 1)
        original_values = dice.values.copy()
        original_result = dice.result
        dice.roll_dice()
        self.assertNotEqual(dice.values, original_values)
        self.assertNotEqual(dice.result, original_result)
        self.assertEqual(dice.result, sum(dice.values))

    def test_draw_die(self):
        surface = MagicMock()  
        x, y, size, value = 100, 100, 60, 3  
        self.dice.draw_die(surface, x, y, size, value)
        surface.draw_rect.assert_called_once()  
        self.assertEqual(surface.draw_circle.call_count, 3) 

    def test_draw(self):
        surface = MagicMock()  
        self.dice.draw(surface)
        self.assertEqual(surface.draw_rect.call_count, 2) 
        total_circles = sum([4 if value == 4 else 5 if value == 5 else 6 if value == 6 else value for value in self.dice.values])
        self.assertEqual(surface.draw_circle.call_count, total_circles)

    def test_invalid_initialization(self):
        with self.assertRaises(TypeError):
            Dice("invalid", 300)  
        with self.assertRaises(TypeError):
            Dice(400, "invalid") 



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








