import unittest
from functools import reduce

from shoe import Shoe
from basic_strategy import Basic_Strategy
from hi_lo import Hi_Lo
from player import Player, Dealer

from blackjack import Blackjack


class BlackjackTest(unittest.TestCase):

	def test_create_deck(self):
		new_shoe = Shoe()
		self.assertEqual(len(new_shoe.shoe), 270)
		# print(new_shoe.shoe)


	def test_draw(self):
		new_shoe = Shoe()
		for x in range(len(new_shoe.shoe)):
			card = new_shoe.draw()
			self.assertEqual(len(card), 2)
		self.assertEqual(len(new_shoe.shoe), 270)


	def test_evaluation(self):
		new_shoe = Shoe(
			number_of_decks=1,
			penetration_percentage=100
			)
		player = Player()
		for card in new_shoe.shoe:
			player.evaluate(card=card)
		self.assertEqual(player.score, 340)


	def test_hi_lo(self):
		counts = Hi_Lo()

		new_shoe = Shoe(
			number_of_decks=2,
			penetration_percentage=65
			)

		self.assertEqual(counts.count, 0)

		for card in ['1c','Jd','Qh','Ks','Ah']:
			counts.count = [card, new_shoe.size]
		self.assertEqual(counts.count, -5)

		self.assertEqual(new_shoe.size, 2)

		for card in ['2d','3h','4s','5h','6c']:
			counts.count = [card, new_shoe.size]
		self.assertEqual(counts.count, 0)

		for card in ['7d','8h','9s','8h','7c']:
			counts.count = [card, new_shoe.size]
		self.assertEqual(counts.count, 0)

		for card in ['2d','3h','4s','5h','6c']:
			counts.count = [card, new_shoe.size]
		self.assertEqual(counts.count, 5)


	def test_blackjack(self):
		bkjk = Blackjack()

		for person in bkjk.people:
			self.assertEqual(person.score, 0)
			self.assertEqual(person.hand, [])

		bkjk.initial_deal()

		for person in bkjk.people:
			self.assertEqual(len(person.hand), 2)
			# self.assertGreaterEqual(person.score, 2)

		bkjk.new_round()

		for person in bkjk.people:
			self.assertEqual(person.score, 0)
			self.assertEqual(person.hand, [])

