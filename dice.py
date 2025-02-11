import pygame
import random

class Dice:
    def __init__(self, width, height):
        self.values = [random.randint(1, 6), random.randint(1, 6)]  # Roll two dice
        self.result = sum(self.values)  # Sum the dice
        self.size = 60  # Size of each die
        self.spacing = 20  # Space between the two dice
        self.total_width = 2 * self.size + self.spacing  # Total width of both dice
        self.x = (width - self.total_width) // 2  # Center the dice horizontally
        self.y = height - 80  # Y position for the dice (moved lower)

    # "Rolls" and randomizes the dice
    def roll_dice(self):
        self.values = [random.randint(1, 6), random.randint(1, 6)]  # Roll two dice
        self.result = sum(self.values)  # Sum the dice

    # Draws the dice onto surface
    def draw_die(self, surface, x, y, size, value):
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