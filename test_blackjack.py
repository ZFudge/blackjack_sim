import unittest

# from blackjack import Blackjack
from cards import Deck

class BlackjackTest(unittest.TestCase):

	def test_create_deck(self):
		new_deck = Deck()
		new_deck.get_decks(8, 65)
		self.assertEqual(len(new_deck.shoe), 270)
		# print(new_deck.shoe)

	def test_draw(self):
		new_deck = Deck()
		new_deck.get_decks(8, 65)
		for x in range(100):
			new_deck.shoe.pop()
		self.assertEqual(len(new_deck.shoe), 170)
		# print(new_deck.shoe)
