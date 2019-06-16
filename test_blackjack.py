import unittest
from functools import reduce

from cards import Shoe
from evaluate import Evaluate
from basic_strategy import Basic_Strategy
from hi_lo import Count

class BlackjackTest(unittest.TestCase):

	def test_create_deck(self):
		new_shoe = Shoe()
		self.assertEqual(len(new_shoe.shoe), 270)
		print(new_shoe.shoe)


	def test_draw(self):
		new_shoe = Shoe()
		for x in range(100):
			new_shoe.shoe.pop()
		self.assertEqual(len(new_shoe.shoe), 170)


	def test_evaluation(self):
		eve = Evaluate()
		new_shoe = Shoe(1, 100)
		evaluated_shoe = [eve.evaluate(x, '0a') for x in new_shoe.shoe]
		summed = reduce(lambda x, y : x + y if type(y) is int else x + sum(y), evaluated_shoe)
		self.assertEqual(summed, 384)

	def test_hi_lo(self):
		counts = Count()

		counts.count_card('Jd')
		counts.count_card('Qh')
		counts.count_card('Ks')
		counts.count_card('Ah')
		counts.count_card('1c')
		self.assertEqual(counts.count, 5)

		counts.count_card('2d')
		counts.count_card('3h')
		counts.count_card('4s')
		counts.count_card('5h')
		counts.count_card('6c')
		self.assertEqual(counts.count, 0)

		counts.count_card('7d')
		counts.count_card('8h')
		counts.count_card('9s')
		counts.count_card('8h')
		counts.count_card('7c')
		self.assertEqual(counts.count, 0)

