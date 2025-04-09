import random

import pygame

import Player
import game_board
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
    running = True

    # Initialize the menu and game state
    # Game states: menu | options | game |
    game_state = "menu"
    menu = Menu(screen, SCREENWIDTH, SCREENHEIGHT)
    player_list = []



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
                game_state = "options"

        elif game_state == "options":
            menu_return = menu.draw_options()
            if menu_return[0] :
                player_count = menu_return[1]
                # If the randomize option was selected, randomize the board
                for i in range(0, player_count):
                    temp = Player.Player(i + 1, 'name' , board.colors[i + 1])
                    player_list.append(temp)

                if menu_return[2]:
                    board.shuffle_board()
                game_state = "game"

        elif game_state == "game":
            # draws the game board
            board.draw_board(screen)
            board.draw_roads(screen)
            board.draw_building(screen)
            choice = menu.draw_game()
            game_bank.draw_bank(screen, SCREENWIDTH, (255, 255, 255))
            player_list[0].bank.draw_bank(screen, SCREENWIDTH, player_list[0].color)
            # If the build buttons was clicked
            if choice[1]:
                game_state = "build"
            # If the next player button is clicked
            elif choice[0]:
                # TO DO: Insert the way to do next person
                player_list.append(player_list.pop(0))
                for player in player_list:
                    print(player.player_id)
                print('\n')
            elif choice[2]:
                game_state = "trade"

        elif game_state == 'build':
            board.draw_board(screen)
            if menu.draw_build(player_bank) == 'exit':
                game_state = 'game'

        elif game_state == 'trade':
            if menu.draw_trade(player_bank)[0]:
                game_state = 'game'

        elif game_state == 'road':
            pass

        elif game_state == 'structure':
            pass

        pygame.display.update()

    # Closes the game safely
    pygame.quit()
