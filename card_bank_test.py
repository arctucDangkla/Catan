import random
from card_bank import CardBank
import unittest
class CardBankTest(unittest.TestCase):
    # INITIALIZATION TESTS #
    # Tests if the game initialization works properly
    def test_init_game(self):
        bank = {
            'Wo': 20,
            'O': 20,
            'S': 20,
            'B': 20,
            'Wh': 20,
            'K': 14,
            'P': 6,
            'V': 5
        }
        game = CardBank('game')
        self.assertEqual(game.bank, bank)

    # Tests if the player initialization works properly
    def test_init_player(self):
        bank = {
            'Wo': 0,
            'O': 0,
            'S': 0,
            'B': 0,
            'Wh': 0,
            'K': 0,
            'P': 0,
            'V': 0
        }
        player = CardBank('player')
        self.assertEqual(player.bank, bank)

    def test_init_invalid1(self):
        with self.assertRaises(TypeError):
            CardBank(123)

    def test_init_invalid2(self):
        with self.assertRaises(TypeError):
            CardBank(541)

    def test_init_invalid3(self):
        with self.assertRaises(ValueError):
            CardBank('error')

    def test_init_invalid4(self):
        with self.assertRaises(ValueError):
            CardBank('invalid')

    # REMOVE TESTS #
    # Tests to remove a card
    def test_remove_one1(self):
        bank = CardBank('game')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        result = bank.bank[rand_resource] - 1
        bank.remove_card(rand_resource)
        for resource in resources:
            if resource == rand_resource:
                self.assertEqual(bank.bank[resource], result)
            elif resource in ('Wo', 'O', 'S', 'B', 'Wh'):
                self.assertEqual(bank.bank[resource], 20)
            elif resource == 'K':
                self.assertEqual(bank.bank[resource], 14)
            elif resource == 'P':
                self.assertEqual(bank.bank[resource], 6)
            else:
                self.assertEqual(bank.bank[resource], 5)

    # Tests to remove a card
    def test_remove_one2(self):
        bank = CardBank('game')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        result = bank.bank[rand_resource] - 1
        bank.remove_card(rand_resource)
        for resource in resources:
            if resource == rand_resource:
                self.assertEqual(bank.bank[resource], result)
            elif resource in ('Wo', 'O', 'S', 'B', 'Wh'):
                self.assertEqual(bank.bank[resource], 20)
            elif resource == 'K':
                self.assertEqual(bank.bank[resource], 14)
            elif resource == 'P':
                self.assertEqual(bank.bank[resource], 6)
            else:
                self.assertEqual(bank.bank[resource], 5)

    # Removes many cards from one single resource
    def test_remove_many_from_one(self):
        bank = CardBank('game')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        remove_num = random.randint(1, bank.bank[rand_resource])
        result = bank.bank[rand_resource] - remove_num
        bank.remove_card(rand_resource, remove_num)
        for resource in resources:
            if resource == rand_resource:
                self.assertEqual(bank.bank[resource], result)
            elif resource in ('Wo', 'O', 'S', 'B', 'Wh'):
                self.assertEqual(bank.bank[resource], 20)
            elif resource == 'K':
                self.assertEqual(bank.bank[resource], 14)
            elif resource == 'P':
                self.assertEqual(bank.bank[resource], 6)
            else:
                self.assertEqual(bank.bank[resource], 5)

    # Tests one remove from multiple resources
    def test_remove_one_from_many(self):
        bank = CardBank('game')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource1 = random.choice(resources)
        rand_resource2 = random.choice(resources)
        while rand_resource1 == rand_resource2:
            rand_resource2 = random.choice(resources)
        result1 = bank.bank[rand_resource1] - 1
        result2 = bank.bank[rand_resource2] - 1
        bank.remove_card(rand_resource1)
        bank.remove_card(rand_resource2)
        for resource in resources:
            if resource == rand_resource1:
                self.assertEqual(bank.bank[resource], result1)
            elif resource == rand_resource2:
                self.assertEqual(bank.bank[resource], result2)
            elif resource in ('Wo', 'O', 'S', 'B', 'Wh'):
                self.assertEqual(bank.bank[resource], 20)
            elif resource == 'K':
                self.assertEqual(bank.bank[resource], 14)
            elif resource == 'P':
                self.assertEqual(bank.bank[resource], 6)
            else:
                self.assertEqual(bank.bank[resource], 5)

    # Tests many (random) removed from many (2) resources
    def test_remove_many_from_many(self):
        bank = CardBank('game')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource1 = random.choice(resources)
        rand_resource2 = random.choice(resources)
        while rand_resource1 == rand_resource2:
            rand_resource2 = random.choice(resources)
        rand_num1 = random.randint(1, bank.bank[rand_resource1])
        rand_num2 = random.randint(1, bank.bank[rand_resource2])
        result1 = bank.bank[rand_resource1] - rand_num1
        result2 = bank.bank[rand_resource2] - rand_num2
        bank.remove_card(rand_resource1, rand_num1)
        bank.remove_card(rand_resource2, rand_num2)
        for resource in resources:
            if resource == rand_resource1:
                self.assertEqual(bank.bank[resource], result1)
            elif resource == rand_resource2:
                self.assertEqual(bank.bank[resource], result2)
            elif resource in ('Wo', 'O', 'S', 'B', 'Wh'):
                self.assertEqual(bank.bank[resource], 20)
            elif resource == 'K':
                self.assertEqual(bank.bank[resource], 14)
            elif resource == 'P':
                self.assertEqual(bank.bank[resource], 6)
            else:
                self.assertEqual(bank.bank[resource], 5)

    # Checks that you cannot remove cards from a balance of zero.
    def test_remove_one_from_zero(self):
        bank = CardBank('player')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        with self.assertRaises(ValueError):
            bank.remove_card(rand_resource)

    # Makes sure that you cannot remove zero
    def test_remove_zero(self):
        bank = CardBank('player')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        with self.assertRaises(ValueError):
            bank.remove_card(rand_resource, 0)

    # Makes sure that type error is raised on invalid int
    def test_remove_invalid_type1(self):
        bank = CardBank('player')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        with self.assertRaises(TypeError):
            bank.remove_card(rand_resource, 'invalid')

    # Makes sure that type error is raised on invalid str
    def test_remove_invalid_type2(self):
        bank = CardBank('player')
        with self.assertRaises(TypeError):
            bank.remove_card(34)

    # Makes sure that value error is raised on improper resource
    def test_remove_invalid_card(self):
        bank = CardBank('player')
        with self.assertRaises(ValueError):
            bank.remove_card('invalid')

    # ADD TESTS #
    # Tests to add a card to a random resource
    def test_add_one(self):
        bank = CardBank('player')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        bank.add_card(rand_resource)
        for resource in resources:
            if resource == rand_resource:
                self.assertEqual(bank.bank[resource], 1)
            else:
                self.assertEqual(bank.bank[resource], 0)

    # Tests to add many cards to one random resource
    def test_add_many_to_one(self):
         bank = CardBank('player')
         resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
         rand_resource = random.choice(resources)
         rand_num = random.randint(1, 15)
         bank.add_card(rand_resource, rand_num)
         for resource in resources:
             if resource == rand_resource:
                 self.assertEqual(bank.bank[resource], rand_num)
             else:
                 self.assertEqual(bank.bank[resource], 0)

    # Tests to add many cards to 2 random resources
    def test_add_many_to_many(self):
         bank = CardBank('player')
         resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
         rand_resource1 = random.choice(resources)
         rand_resource2 = random.choice(resources)
         while rand_resource1 == rand_resource2:
             rand_resource2 = random.choice(resources)
         rand_num1 = random.randint(1, 15)
         rand_num2 = random.randint(1, 15)
         bank.add_card(rand_resource1, rand_num1)
         bank.add_card(rand_resource2, rand_num2)
         for resource in resources:
             if resource == rand_resource1:
                 self.assertEqual(bank.bank[resource], rand_num1)
             elif resource == rand_resource2:
                 self.assertEqual(bank.bank[resource], rand_num2)
             else:
                 self.assertEqual(bank.bank[resource], 0)

    # Tests to see if error raises when adding zero
    def test_add_zero(self):
        bank = CardBank('player')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        with self.assertRaises(ValueError):
            bank.add_card(rand_resource, 0)

    # Tests to see if error raises when invalid resource type
    def test_add_invalid_type1(self):
        bank = CardBank('player')
        with self.assertRaises(TypeError):
            bank.add_card(34)

    # Tests to see if error raises when invalid number type
    def test_add_invalid_type2(self):
        bank = CardBank('player')
        with self.assertRaises(TypeError):
            bank.add_card('Wo', 'Invalid.')

    # Tests to see if value error raises on invalid card
    def test_add_invalid_card(self):
        bank = CardBank('player')
        with self.assertRaises(ValueError):
            bank.add_card('Invalid')

    # Tests to see if error is raised when tyring to add more than max
    def test_add_max(self):
        bank = CardBank('game')
        resources = ['Wo', 'O', 'S', 'B', 'Wh', 'K', 'P', 'V']
        rand_resource = random.choice(resources)
        with self.assertRaises(ValueError):
            bank.add_card(rand_resource)