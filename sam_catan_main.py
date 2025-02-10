import pygame
import button
import game_board
pygame.init()

# Screen Size
SCREENWIDTH = 1000
SCREENHEIGHT = SCREENWIDTH * .80 #800 pixels

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Catan")
running = True

# Initialize Buttons
rand_button = button.Button(SCREENWIDTH * 0.75, SCREENHEIGHT * 7/8, "images/button_random.png")
begin_button = button.Button(SCREENWIDTH * 0.06, SCREENHEIGHT * 7/8, "images/button_beginner.png")

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
    # Checks for button presses
    if rand_button.draw(screen):
        board.shuffle_board()
    if begin_button.draw(screen):
        board.beginner_board()


    pygame.display.update()

# Closes the game safely
pygame.quit()