import unittest
from functools import reduce

from shoe import Shoe
from evaluate import Evaluate
from basic_strategy import Basic_Strategy
from hi_lo import Count
from player import Player


class BlackjackTest(unittest.TestCase):

	def test_create_deck(self):
		new_shoe = Shoe()
		self.assertEqual(len(new_shoe.shoe), 270)
		print(new_shoe.shoe)


	def test_draw(self):
		new_shoe = Shoe()
		for x in range(100):
			new_shoe.draw()
		self.assertEqual(len(new_shoe.shoe), 170)


	def test_evaluation(self):
		eve = Evaluate()
		new_shoe = Shoe(number_of_decks=1, penetration_percentage=100)
		player = Player()
		for card in new_shoe.shoe:
			eve.evaluate_card_value(
				person=player,
				card=card
				)
		self.assertEqual(player.score, 340)


	def test_hi_lo(self):
		counts = Count()
		new_shoe = Shoe(number_of_decks=2, penetration_percentage=65)

		for x in ['1c','Jd','Qh','Ks','Ah']:
			counts.count_card(x)
		self.assertEqual(counts.count, 5)
		self.assertEqual(new_shoe.deck_count, 2)

		for x in ['2d','3h','4s','5h','6c']:
			counts.count_card(x)
		self.assertEqual(counts.count, 0)

		for x in ['7d','8h','9s','8h','7c']:
			counts.count_card(x)
		self.assertEqual(counts.count, 0)

