import random

import pygame
import button
import game_board
import dice

import longest_path


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

    # Initialize Buttons
    dice_button = button.Button(screen, dice_vals.x, dice_vals.y, "none", dice_vals.total_width, dice_vals.size)

    # Initialize the Board
    board = game_board.Board(screen, SCREENWIDTH, SCREENHEIGHT)
    board.draw_board(screen, dice_vals.result)


    # Here just for visual testing
    """num = random.randint(0, 12)
    if num == 6:
        num = 1
    other_num = random.randint(0, len(board.grid.node_list[num])-1)"""

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

    show_buildable_road = False
    show_buildable_house = False
    No_builds = True

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

        # draws the game board
        board.draw_board(screen, dice_vals.result)
        board.draw_roads(screen)
        board.draw_building(screen)


        if show_buildable_road:
            board.find_buildable_road(board.cur_player)
            board.draw_buildable(board.grid.build_able, screen)
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
                    print(f"{longest} is from player {longest_player}")


        elif show_buildable_house:
            board.find_buildable_house(board.cur_player)
            board.draw_buildable(board.grid.build_able, screen)
            for x in board.grid.build_able:
                if x.button.draw():
                    x.player = board.cur_player
                    board.grid.buildable_road(board.cur_player)


        # Draws the dice
        dice_vals.draw_die(screen, dice_vals.x, dice_vals.y, dice_vals.size, dice_vals.values[0])  # Draw first die
        dice_vals.draw_die(screen, dice_vals.x + dice_vals.size + dice_vals.spacing, dice_vals.y, dice_vals.size,
                           dice_vals.values[1])  # Draw second d
        # Checks for dice roll
        if dice_button.draw():
            dice_vals.roll_dice()

        if next_button.draw():
            board.next_player()

        if build_toggle_button.draw():
            show_buildable_house, show_buildable_road, No_builds = show_buildable_road, No_builds, show_buildable_house

        pygame.display.update()

    # Closes the game safely
    pygame.quit()
