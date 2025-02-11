import pygame
import button
import game_board
import dice
pygame.init()

# Screen Size
SCREENWIDTH = 1000
SCREENHEIGHT = SCREENWIDTH * .80 #800 pixels

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Catan")
dice_vals = dice.Dice(SCREENWIDTH, SCREENHEIGHT)
running = True

# Initialize Buttons
rand_button = button.Button(SCREENWIDTH * 0.75, SCREENHEIGHT * 7/8, "images/button_random.png")
begin_button = button.Button(SCREENWIDTH * 0.06, SCREENHEIGHT * 7/8, "images/button_beginner.png")
dice_button = button.Button(dice_vals.x, dice_vals.y, "none", dice_vals.total_width, dice_vals.size)

# Initialize the Board
board = game_board.Board(SCREENWIDTH, SCREENHEIGHT)

while running:
    # Makes the background for the game.
    screen.fill((79, 166, 235))

    # Check for events, such as closing game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draws the game board
    board.draw_board(screen)

    # Draws the dice
    dice_vals.draw_die(screen, dice_vals.x, dice_vals.y, dice_vals.size, dice_vals.values[0])  # Draw first die
    dice_vals.draw_die(screen, dice_vals.x + dice_vals.size + dice_vals.spacing, dice_vals.y, dice_vals.size,
                       dice_vals.values[1])  # Draw second die
    # Checks for randomization press
    if rand_button.draw(screen):
        board.shuffle_board()

    # Checks for beginner board press
    if begin_button.draw(screen):
        board.beginner_board()

    # Checks for dice roll
    if dice_button.draw(screen):
        dice_vals.roll_dice()

    pygame.display.update()

# Closes the game safely
pygame.quit()
