import pygame
from button import Button

class CardBank:
    # User can either be 'game' or 'player'
    # where game is for the game's bank
    # and player is to track a players resources
    def __init__(self, user):
        if not isinstance(user, str):
            raise TypeError('Invalid Type')
        if user.lower() == 'game':
            self.bank = {
                'Wo': 20,
                'O': 20,
                'S': 20,
                'B': 20,
                'Wh': 20,
                'K': 14,
                'P': 6,
                'V': 5
            }
            self.user = user.lower()
        elif user.lower() == 'player':
            self.bank = {
                'Wo': 0,
                'O': 0,
                'S': 0,
                'B': 0,
                'Wh': 0,
                'K': 0,
                'P': 0,
                'V': 0
            }
            self.user = user.lower()
        else:
            raise ValueError('Invalid input')

    # Num has a default value of 1, to remove just 1 card.
    # Card should match one of the keys from the dictionary.
    def remove_card(self, card, num = 1):
        #Ensures that types and number of cards are valid.
        if not isinstance(card, str) or not isinstance(num, int):
            raise TypeError('Invalid Type')
        if num <= 0:
            raise ValueError('Cannot remove 0 or less cards')

        # Checks if the string exists in the dictionary
        if card not in self.bank.keys():
            raise ValueError('Invalid card')
        else:
            # Checks to ensure there are enough cards to remove
            if self.bank[card] >= num:
                self.bank[card] -= num
            else:
                raise ValueError('Cannot remove any more cards.')

    # Num has a default value of 1, to remove just 1 card.
    # Card should match one of the keys from the dictionary.
    def add_card(self, card, num = 1):
        # Ensures that types and number of cards are valid.
        if not isinstance(card, str) or not isinstance(num, int):
            raise TypeError('Invalid Type')
        if num <= 0:
            raise ValueError('Cannot add 0 or less cards')

        # Checks if the string exists in the dictionary
        if card not in self.bank.keys():
            raise ValueError('Invalid card')
        # A game bank cannot have more than starting amount of cards
        elif self.user == 'game':
            if card in ('Wo', 'O', 'S', 'B', 'Wh') and self.bank[card] == 20 or self.bank[card] + num > 20:
                raise ValueError('Cannot add more cards.')
            elif card == 'K' and self.bank[card] == 14 or self.bank[card] + num > 14:
                raise ValueError('Cannot add more cards.')
            elif card == 'P' and self.bank[card] == 6 or self.bank[card] + num > 6:
                raise ValueError('Cannot add more cards.')
            elif card == 'V' and self.bank[card] == 5 or self.bank[card] + num > 5:
                raise ValueError('Cannot add more cards.')
            else:
                self.bank[card] += num
        else:
            self.bank[card] += num

    # Draws an individual card as a Button
    #sheep_button = button.Button(0, SCREENHEIGHT * .10, "images/resources_sheep.png", 0, 0, 0.2)
    # origin width = 326 | scaled width = 65.2
    # origin height = ??? | scaled height = 95.8
    def draw_card(self, card, x, y, screen):
        if card == 'Wo':
            return Button(x, y, "images/resources_wood.png", 0, 0, 0.2)
        elif card == 'O':
            return Button(x, y, "images/resources_ore.png", 0, 0, 0.2)
        elif card == 'S':
            return Button(x, y, "images/resources_sheep.png", 0, 0, 0.2)
        elif card == 'B':
            return Button(x, y, "images/resources_brick.png", 0, 0, 0.2)
        elif card == 'Wh':
            return Button(x, y, "images/resources_wheat.png", 0, 0, 0.2)
        else:
            return Button(x, y, "images/devcard_back.png", 0, 0, 0.2)

        # Draws the bank with all cards
    def draw_bank(self, screen, screen_width):
        # If the bank is of type game, draw the bank on right side
        # If the bank is of type player, draw the bank of left side
        # Make sure to display number of cards on the corresponding sides!!! #
        resources = ['Wo','O', 'S', 'B', 'Wh', 'D']
        if self.user == 'player':
            x = 0
        else:
            x = screen_width - 66 # 65 is width of card
        y = 0
        for resource in resources:
            temp = self.draw_card(resource, x, y, screen)
            temp.draw(screen)
            y += 100

