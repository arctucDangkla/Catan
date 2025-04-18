import pygame
from button import Button
import card_bank


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
        self.beginner = Button(screen, 50, 350, "images/buttons/button_beginner.png", 0, 0, 0.8)
        self.random = Button(screen, 550, 350, "images/buttons/button_random.png", 0, 0, 0.8)
        self.threeplayers = Button(screen, 50, 100, "images/buttons/button_3players.png", 0, 0, 0.8)
        self.fourplayers = Button(screen, 550, 100, "images/buttons/button_4players.png", 0, 0, 0.8)
        self.players = 4
        self.randomize = False
        # Buttons for the game screen:
        self.next_player = Button(screen, 750, 700, "images/buttons/button_next-player.png")
        self.exit = Button(screen, 750, 700, "images/buttons/button_exit.png")
        self.build = Button(screen, 25, 730, "images/buttons/button_build.png")
        self.trade = Button(screen, 25, 650, "images/buttons/button_trade.png")
        # Buttons for the build screen:
        self.road = Button(screen, 775, 670, "images/buttons/button_road.png")
        self.settlement = Button(screen, 775, 530, "images/buttons/button_settlement.png")
        self.devcard = Button(screen, 775, 740, "images/buttons/button_dev-card.png")
        self.city = Button(screen, 775, 600, "images/buttons/button_city.png")
        # variables for the trade screen:
        self.reset = False
        self.button_give = {
            'Wo': [],
            'O': [],
            'S': [],
            'B': [],
            'Wh': []
        }
        self.button_receive = {
            'Wo': [],
            'O': [],
            'S': [],
            'B': [],
            'Wh': []
        }
        self.give = {
            'Wo': 0,
            'O': 0,
            'S': 0,
            'B': 0,
            'Wh': 0
        }
        self.receive = {
            'Wo': 0,
            'O': 0,
            'S': 0,
            'B': 0,
            'Wh': 0
        }
        i = 125
        for resource in self.give:
            minus = Button(self.screen, i - 40, 90, "images/buttons/button_delete.png", 0, 0, 0.5)
            card = card_bank.draw_card(resource, i, 90, self.screen)
            add = Button(self.screen, i + 65, 90, "images/buttons/button_add.png", 0, 0, 0.5)
            self.button_give[resource].append(minus)
            self.button_give[resource].append(card)
            self.button_give[resource].append(add)
            i += 160
        i = 125
        for resource in self.receive:
            minus = Button(self.screen, i - 40, 500, "images/buttons/button_delete.png", 0, 0, 0.5)
            card = card_bank.draw_card(resource, i, 500, self.screen)
            add = Button(self.screen, i + 65, 500, "images/buttons/button_add.png", 0, 0, 0.5)
            self.button_receive[resource].append(minus)
            self.button_receive[resource].append(card)
            self.button_receive[resource].append(add)
            i += 160
        self.cont = Button(self.screen, 750, 700, "images/buttons/button_continue.png")
        self.bank_button = Button(self.screen, 400, 700, "images/buttons/button_bank.png")
        # Error values
        self.error_rect = pygame.Rect(350, 350, 390, 45)
        # Player pick buttons
        self.player1 = Button(self.screen, 100, 740, "images/buttons/button_player1.png")
        self.player2 = Button(self.screen, 300, 740, "images/buttons/button_player2.png")
        self.player3 = Button(self.screen, 500, 740, "images/buttons/button_player3.png")
        self.player4 = Button(self.screen, 700, 740, "images/buttons/button_player4.png")
        self.player_choice = [False, False, False, False, False] # Continue, p1, p2, p3, p4

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, self.text_col)
        self.screen.blit(img, (x, y))

    def draw_main(self):
        self.logo.draw()
        return self.start.draw()

    def draw_options(self) -> [bool, int, bool]:
        self.start.rect.y = 625
        if self.threeplayers.draw():
            self.players = 3
        if self.fourplayers.draw():
            self.players = 4
        # If the selected player amount is 3, show that it is selected
        if self.players == 3:
            self.draw_text("SELECTED", self.threeplayers.rect.left + 100, self.threeplayers.rect.bottom)
        else:
            self.draw_text("SELECTED", self.fourplayers.rect.left + 100, self.fourplayers.rect.bottom)
        if self.random.draw():
            self.randomize = True
        if self.beginner.draw():
            self.randomize = False
        if self.randomize:
            self.draw_text("SELECTED", self.random.rect.left + 100, self.random.rect.bottom)
        else:
            self.draw_text("SELECTED", self.beginner.rect.left + 100, self.beginner.rect.bottom)
        # If the player clicks continue, return the values to be assessed.
        return [self.start.draw(), self.players, self.randomize]

    # Draws buttons that are on the game screen.
    # [Next player, building mode, trading mode]
    def draw_game(self) -> [bool, bool, bool]:
        return [self.next_player.draw(), self.build.draw(), self.trade.draw()]

    # Draws a menu to choose what to build. If not enough resources, show a popup.
    def draw_build(self):
        # player.bank.drawBank(..)
        self.exit.rect.topleft = (50, 700)

        if self.exit.draw():
            return 'exit'
        if self.settlement.draw():
            # if check amount = true
            # return 'settlement'
            # else draw_popup
            return 1
        if self.city.draw():
            pass
        if self.road.draw():
            return 2
        if self.devcard.draw():
            pass
        #return [self.exit.draw(), self.settlement.draw(), self.city.draw(), self.road.draw(), self.devcard.draw()]

    # Draws the buildable locations
    def draw_building(self, board):
        board.draw_buildable(board.grid.build_able, self.screen)
        for x in board.grid.build_able:
            if x.button.draw():
                x.player = 1
                board.grid.buildable_road(1)

    # [choice:str, give:dict, receive:dict] give and receive are
    # to be called with card_bank.add and remove
    def draw_trade(self, bank):
        self.cont.rect.topleft = (750, 700)
        if self.reset:
            for resource in self.receive:
                self.receive[resource] = 0
                self.give[resource] = 0
            self.reset = False
        self.exit.rect.topleft = (50, 700)
        self.draw_text('You will give:', 350, 0)
        self.draw_text('You will receive:', 350, 425)
        for resource in self.button_give:
            for i in range (3):
                if i == 0 and self.button_give[resource][i].draw() and self.give[resource] > 0:
                    self.give[resource] -= 1
                if i == 1:
                    self.button_give[resource][i].draw()
                if i == 2 and self.button_give[resource][i].draw():
                    self.give[resource] += 1
            self.draw_text(str(self.give[resource]), self.button_give[resource][1].rect.left, self.button_give[resource][1].rect.bottom)
        for resource in self.button_receive:
            for i in range (3):
                if i == 0 and self.button_receive[resource][i].draw() and self.receive[resource] > 0:
                    self.receive[resource] -= 1
                if i == 1:
                    self.button_receive[resource][i].draw()
                if i == 2 and self.button_receive[resource][i].draw():
                    self.receive[resource] += 1
            self.draw_text(str(self.receive[resource]), self.button_receive[resource][1].rect.left, self.button_receive[resource][1].rect.bottom)
        if self.exit.draw():
            self.reset = True
            return['exit', self.give, self.receive]
        elif self.cont.draw():
            self.reset = True
            return['continue', self.give, self.receive]
        elif self.bank_button.draw():
            self.reset = True
            return['bank', self.give, self.receive]
        else:
            return['none', self.give, self.receive]

    # Returns a list with bools: [continue, p1, p2, p3, p4]
    # Num is the number of players
    # mode is the mode in which it is running: trade | bank
    def draw_player_pick(self, num, mode):
        self.cont.rect.topleft = (750, 600)
        if self.player_choice[0]:
            self.player_choice = [False, False, False, False, False]
        if mode == 'trade':
            self.player1.rect.topleft = (100, 450)
            self.player2.rect.topleft = (300, 450)
            self.player3.rect.topleft = (500, 450)
            self.player4.rect.topleft = (700, 450)
            if self.player1.draw():
                self.player_choice = [True, True, False, False, False]
                return self.player_choice
            elif self.player2.draw():
                self.player_choice = [True, False, True, False, False]
                return self.player_choice
            elif self.player3.draw():
                self.player_choice = [True, False, False, True, False]
                return self.player_choice
            elif num == 4 and self.player4.draw():
                self.player_choice = [True, False, False, False, True]
                return self.player_choice
            elif self.exit.draw():
                self.player_choice = [True, False, False, False, False]
            return self.player_choice
        elif mode == 'bank':
            self.player1.rect.topleft = (100, 740)
            self.player2.rect.topleft = (300, 740)
            self.player3.rect.topleft = (500, 740)
            self.player4.rect.topleft = (700, 740)

            # Writes selected under players who have been clicked
            if self.player_choice[1]:
                self.draw_text("SELECTED", self.player1.rect.left, self.player1.rect.top - 40)
            if self.player_choice[2]:
                self.draw_text("SELECTED", self.player2.rect.left, self.player2.rect.top - 40)
            if self.player_choice[3]:
                self.draw_text("SELECTED", self.player3.rect.left, self.player3.rect.top - 40)
            if self.player_choice[4]:
                self.draw_text("SELECTED", self.player4.rect.left, self.player4.rect.top - 40)

            # Handles the click of buttons on the screen.
            player1_click = self.player1.draw()
            player2_click = self.player2.draw()
            player3_click = self.player3.draw()

            if player1_click and self.player_choice[1]:
                self.player_choice[1] = False
            elif player1_click and not self.player_choice[1]:
                self.player_choice[1] = True
            if player2_click and self.player_choice[2]:
                self.player_choice[2] = False
            elif player2_click and not self.player_choice[2]:
                self.player_choice[2] = True
            if player3_click and self.player_choice[3]:
                self.player_choice[3] = False
            elif player3_click and not self.player_choice[3]:
                self.player_choice[3] = True
            if num == 4:
                player4_click = self.player4.draw()
                if player4_click and self.player_choice[4]:
                    self.player_choice[4] = False
                elif player4_click and not self.player_choice[4]:
                    self.player_choice[4] = True
            if self.cont.draw():
                self.player_choice[0] = True
            return self.player_choice



    # A message for popup for whenever a user tries to build something
    # without the minimum amount of resources required.
    # pygame.time.delay(milliseconds) to stop the time.
    def draw_popup(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.error_rect)
        self.draw_text('An error has occurred.', 350, 350)
        pygame.display.update()
        pygame.time.delay(2000)
