import math
import pygame
import random

# Screen Size
SCREENWIDTH = 1000
SCREENHEIGHT = int(SCREENWIDTH * 0.80)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Catan")
clock = pygame.time.Clock()
running = True

# Font for rendering numbers and dice results
font = pygame.font.Font(None, 36)  # Default font, size 36

# Dice roll variables
dice_result = None
dice_values = [1, 1]  # Stores the values of the two dice

# Function to calculate hexagon points
def calculate_hexagon(center_x, center_y, radius):
    points = []
    for i in range(6):  # 6 sides in a hexagon
        angle_deg = 60 * i - 30  # Start at -30° to align the flat side at the top
        angle_rad = math.radians(angle_deg)
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)
        points.append((x, y))
    return points

# Function to roll the dice
def roll_dice():
    global dice_result, dice_values
    dice_values = [random.randint(1, 6), random.randint(1, 6)]  # Roll two dice
    dice_result = sum(dice_values)  # Sum the dice
    print(f"Dice Roll: {dice_values} (Total: {dice_result})")  # Optional: Print result to console

# Function to draw a single die
def draw_die(surface, x, y, size, value):
    die_color = (255, 255, 255)  # White die
    dot_color = (0, 0, 0)  # Black dots
    pygame.draw.rect(surface, die_color, (x, y, size, size), border_radius=10)  # Draw die
    if value == 1:
        pygame.draw.circle(surface, dot_color, (x + size // 2, y + size // 2), size // 8)
    elif value == 2:
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + 3 * size // 4), size // 8)
    elif value == 3:
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + size // 2, y + size // 2), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + 3 * size // 4), size // 8)
    elif value == 4:
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + 3 * size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + 3 * size // 4), size // 8)
    elif value == 5:
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + size // 2, y + size // 2), size // 8)
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + 3 * size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + 3 * size // 4), size // 8)
    elif value == 6:
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + size // 2), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + size // 2), size // 8)
        pygame.draw.circle(surface, dot_color, (x + size // 4, y + 3 * size // 4), size // 8)
        pygame.draw.circle(surface, dot_color, (x + 3 * size // 4, y + 3 * size // 4), size // 8)

# Function to draw the game board with numbers, colored hexagons, and the robber
def game_board():
    # Colors for the board
    bg_color = (79, 166, 235)  # Light blue background
    number_color = (0, 0, 0)  # Black color for numbers
    robber_color = (50, 50, 50)  # Dark gray for the robber

    # Resource colors
    brick_color = (178, 34, 34)  # Red/Brown for brick
    wood_color = (34, 139, 34)  # Green for wood
    wheat_color = (255, 223, 0)  # Yellow for wheat
    sheep_color = (144, 238, 144)  # Light green for sheep
    ore_color = (128, 128, 128)  # Gray for ore
    desert_color = (210, 180, 140)  # Light brown for desert

    # Size info for the hexagon
    start_x = SCREENWIDTH * 0.35
    start_y = SCREENHEIGHT / 6
    hex_size = SCREENHEIGHT / 10
    hex_diff = 150  # Horizontal spacing between hexagons

    # Numbers and resources for each hexagon (standard Catan distribution)
    numbers = [  # Sample board
        [10, 2, 9],  # First row
        [12, 6, 4, 10],  # Second row
        [9, 11, None, 3, 8],  # Third row (None for desert)
        [8, 3, 4, 5],  # Fourth row
        [5, 6, 11]  # Fifth row
    ]

    # Resources for each hexagon
    resources = [  # Sample board
        [ore_color, sheep_color, wood_color],  # 1
        [wheat_color, brick_color, sheep_color, brick_color],  # 2
        [wheat_color, wood_color, desert_color, wood_color, ore_color],  # 3
        [wood_color, ore_color, wheat_color, sheep_color],  # 4
        [brick_color, wheat_color, sheep_color]  # 5
    ]

    screen.fill(bg_color)  # Fill the screen with the background color

    robber_position = None  # Track the position of the robber

    # Draw hexagons and numbers
    for row in range(5):
        for col in range(len(numbers[row])):
            # Calculate hexagon center
            if row == 0:
                center_x = start_x + hex_diff * col
                center_y = start_y
            elif row == 1:
                center_x = start_x - hex_size + 5 + hex_diff * col
                center_y = start_y + 125
            elif row == 2:
                center_x = start_x - hex_size * 2 + 10 + hex_diff * col
                center_y = start_y + 250
            elif row == 3:
                center_x = start_x - hex_size + 5 + hex_diff * col
                center_y = start_y + 375
            elif row == 4:
                center_x = start_x + hex_diff * col
                center_y = start_y + 500

            hex_color = resources[row][col]
            pygame.draw.polygon(screen, hex_color, calculate_hexagon(center_x, center_y, hex_size))

            # Draw numbers
            if numbers[row][col] is not None:
                number_text = font.render(str(numbers[row][col]), True, number_color)
                text_rect = number_text.get_rect(center=(center_x, center_y))
                screen.blit(number_text, text_rect)
            else:
                # Place the robber on the desert tile
                robber_position = (int(center_x), int(center_y))

    # Draw the robber
    if robber_position:
        pygame.draw.circle(screen, robber_color, robber_position, int(hex_size * 0.3))

    # Draw the dice
    die_size = 60  # Size of each die
    die_spacing = 20  # Space between the two dice
    dice_x = SCREENWIDTH - 200  # X position for the dice
    dice_y = SCREENHEIGHT - 100  # Y position for the dice

    draw_die(screen, dice_x, dice_y, die_size, dice_values[0])  # Draw first die
    draw_die(screen, dice_x + die_size + die_spacing, dice_y, die_size, dice_values[1])  # Draw second die

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Check for key press
            if event.key == pygame.K_SPACE:  # Roll dice when spacebar is pressed
                roll_dice()

    game_board()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
