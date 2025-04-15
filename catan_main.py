import random
import Player
import pygame
import button
import game_board
import longest_path
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



    #
    # Initialize the Board
    board = game_board.Board(screen, SCREENWIDTH, SCREENHEIGHT)
    game_bank = CardBank("game")
    player_bank = CardBank("player")



    # Here just for visual testing

    temp_player_count = 8
    while temp_player_count != 0:
        num = random.randint(0, len(board.grid.node_list)-1)
        if num == 6:
            num = 1
        other_num = random.randint(0, len(board.grid.node_list[num])-1)


        x = board.grid.node_list[num][other_num]
        if x.player == 0:
            x.player = board.cur_player

            picked = False
            picked_road = 0
            while not picked:
                picked_road = random.randint(0, len(x.roads)-1)
                if x.roads[picked_road].player == 0:
                    picked = True
            x.roads[picked_road].player = board.cur_player

            board.next_player()
            temp_player_count -= 1

    longest = 4
    longest_player = 0

    next_button = button.Button(screen, SCREENWIDTH*.9, SCREENHEIGHT*.9, "none", SCREENWIDTH*.1, SCREENHEIGHT*.1)
    build_toggle_button = button.Button(screen, SCREENWIDTH * .8, SCREENHEIGHT * .9, "none", SCREENWIDTH * .1,
                                SCREENHEIGHT * .1)
    while running:

        # Makes the background for the game.
        screen.fill((79, 166, 235))

        # Check for events, such as closing game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Prints Title Screen
        if game_state == "menu":
            if menu.draw_main():
                game_state = "options"

        # Prints Options Screen
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

        # Prints Game Board with selected Settings
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
                board.cur_player = player_list[0].player_id

            elif choice[2]:
                game_state = "trade"

        # Allows player to spend resources to build Roads and Structures
        elif game_state == 'build':
            choice = menu.draw_build(player_bank)
            board.draw_board(screen)
            board.draw_roads(screen)
            board.draw_building(screen)

            # Sets game state to game
            if choice == 'exit':
                game_state = 'game'

            # Sets game state to structure
            elif choice == 1:
                game_state = 'structure'

            # Sets game state to 'road'
            elif choice == 2:
                game_state = 'road'

        # Allows players to trade
        elif game_state == 'trade':

            # Sets game state to game
            if menu.draw_trade(player_bank)[0]:
                game_state = 'game'

        # allows player to place roads
        elif game_state == 'road':
            board.draw_board(screen)
            board.draw_roads(screen)
            board.draw_building(screen)

            board.find_buildable_road(board.cur_player)
            board.draw_buildable(board.grid.build_able, screen)

            # allows for continual placing of roads
            for x in board.grid.build_able:

                if x.button.draw():
                    x.player = board.cur_player
                    board.grid.buildable_road(board.cur_player)

                    for road in board.grid.edge_list:

                        if road.player == board.cur_player:
                            val = longest_path.temp_name(road, board.cur_player, [], [])

                            if val > longest:
                                longest = val

                                longest_player = board.cur_player

            # Sets game state to build
            if menu.exit.draw():
                game_state = 'build'

        # allows player to place building
        elif game_state == 'structure':

            board.draw_board(screen)
            board.draw_roads(screen)
            board.draw_building(screen)


            board.find_buildable_house(board.cur_player)

            board.draw_buildable(board.grid.build_able, screen)
            for x in board.grid.build_able:
                if x.button.draw():
                    x.player = board.cur_player
                    board.grid.buildable_road(board.cur_player)

            if menu.exit.draw():
                game_state = 'build'


        pygame.display.update()


    # Closes the game safely
    pygame.quit()
