import unittest
from functools import reduce


# from blackjack import Blackjack
from cards import Deck
from evaluate import Evaluate


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


	def test_evaluation(self):
		eve = Evaluate()
		new_deck = Deck()
		new_deck.get_decks(1, 100)
		evaluated_shoe = [eve.evaluate(x, '0a') for x in new_deck.shoe]
		summed = reduce(lambda x, y : x + y if type(y) is int else x + sum(y), evaluated_shoe)
		self.assertEqual(summed, 384)

