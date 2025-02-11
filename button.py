import pygame

class Button:
    def __init__(self, x, y, image:str="none", width=0, height=0, scale=1.0):
        # If the button is to be transparent, make a transparent surface
        if image.lower() == "none":
            self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            self.image = self.image.convert_alpha()
        # Otherwise make a button out of the image
        else:
            img = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    # Function that draws the button onto the screen.
    def draw(self, screen):
        action = False
        # Gets the mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions.
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        # Once the button is released, set clicked to false.
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Actually draws the button
        screen.blit(self.image, self.rect.topleft)
        return action
