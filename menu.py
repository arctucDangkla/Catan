import pygame
from button import Button

class Menu:
    def __init__(self, screen, width, height):
        # Defaults for the menu
        self.screen = screen
        self.width = width
        self.height = height
        self.text_col = (255, 255, 255)
        self.font = pygame.font.SysFont('ebrima', 40)
        # Buttons for the main menu:
        self.start = Button(screen, 320, 445, "images/buttons/button_start.png")
        self.logo = Button(screen, 230, 120, "images/catan_logo.png", 0, 0, 1.2)
        # Buttons for the options menu:
        self.beginner = Button(screen, 50, 500, "images/buttons/button_beginner.png", 0, 0, 0.8)
        self.random = Button(screen, 550, 500, "images/buttons/button_random.png", 0, 0, 0.8)
        self.threeplayers = Button(screen, 50, 100, "images/buttons/button_3players.png", 0, 0, 0.8)
        self.fourplayers = Button(screen, 550, 100, "images/buttons/button_4players.png", 0, 0, 0.8)

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, self.text_col)
        self.screen.blit(img, (x, y))

    def draw_main(self):
        self.logo.draw()
        return self.start.draw()

    def draw_options(self, board):
        if self.threeplayers.draw():
            players = 3
            self.draw_text("SELECTED", self.threeplayers.rect.centerx, self.threeplayers.rect.centery)
        if self.fourplayers.draw():
            players = 4
        self.random.draw()
        self.beginner.draw()