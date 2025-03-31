import random

import pygame
import button
import game_board
import dice
from card_bank import CardBank
from menu import Menu


if __name__ == "__main__":
    pygame.init()


    # Screen Size
    SCREENWIDTH = 1000
    SCREENHEIGHT = SCREENWIDTH * .80  # 800 pixels
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Catan")
    dice_vals = dice.Dice(SCREENWIDTH, SCREENHEIGHT)
    running = True

    # Initialize the menu and game state
    # Game states: menu | options | game |
    game_state = "menu"
    menu = Menu(screen, SCREENWIDTH, SCREENHEIGHT)


    # Initialize Buttons
    dice_button = button.Button(screen, dice_vals.x, dice_vals.y, "none", dice_vals.total_width, dice_vals.size)

    # Initialize the Board
    board = game_board.Board(screen, SCREENWIDTH, SCREENHEIGHT)
    game_bank = CardBank("game")
    player_bank = CardBank("player")



    # Here just for visual testing
    num = random.randint(0, 12)
    if num == 6:
        num = 1
    other_num = random.randint(0, len(board.grid.node_list[num])-1)

    x = board.grid.node_list[num][other_num]
    x.player = 1
    x.roads[0].player = 1
    x.roads[1].player = 1


    y = board.grid.node_list[6][2]
    y.player = 1
    y.roads[0].player = 1

    board.find_buildable(1)

    show_buildable = True






    while running:

        # Makes the background for the game.
        screen.fill((79, 166, 235))

        # Check for events, such as closing game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state == "menu":
            if menu.draw_main():
                game_state = "game"
        elif game_state == "options":
            menu.draw_options(board)
        elif game_state == "game":
            # draws the game board
            board.draw_board(screen, dice_vals.result)
            board.draw_roads(screen)
            board.draw_building(screen)

            board.draw_buildable(board.grid.build_able, screen)

            if show_buildable:
                board.draw_buildable(board.grid.build_able, screen)
                for x in board.grid.build_able:
                    if x.button.draw():
                        x.player = 1
                        board.grid.buildable_road(1)
            # Draws the dice
            dice_vals.draw_die(screen, dice_vals.x, dice_vals.y, dice_vals.size, dice_vals.values[0])  # Draw first die
            dice_vals.draw_die(screen, dice_vals.x + dice_vals.size + dice_vals.spacing, dice_vals.y, dice_vals.size,
                               dice_vals.values[1])  # Draw second die
            # Draws the card banks
            game_bank.draw_bank(screen, SCREENWIDTH, (255, 255, 255))
            player_bank.draw_bank(screen, SCREENWIDTH, (255, 0, 0))
            # Checks for dice roll
            if dice_button.draw():
                dice_vals.roll_dice()

        pygame.display.update()

    # Closes the game safely
    pygame.quit()
