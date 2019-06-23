from basic_strategy import Basic_Strategy
from evaluate import Evaluate
from hi_lo import Hi_Lo


class Person(Evaluate):
	def __init__(self):
		self.score = 0
		self.hand = []

	def new_hand(self):
		self.hand = []

	def evaluate(self, card):
		card = card[0]
		self.score = self.evaluate_card_value(
			score=self.score,
			card=card,
			)


class Dealer(Person):
	def deal(self, shoe, person, num_of_cards=1):
		for x in range(num_of_cards):
			card = shoe.draw()
			person.hand.append(card)
			person.evaluate(evaluate_card_value)


class Player(Person):
	def __init__(self, bankroll=1000, bet_unit=5, bet_spread=12):
		Person.__init__(self)
		self._bankroll = bankroll
		self._bet_unit = bet_unit
		self._bet_spread = bet_spread


	@property
	def bankroll(self):
		return self._bankroll

	@bankroll.setter
	def bankroll_increment(self, value):
		self._bankroll += value

	@property
	def bet_unit(self):
		return self._bet_unit

	@bet_unit.setter
	def bet_unit(self, value):
		self._bet_unit = value

	@property
	def bet_spread(self):
		return self._bet_spread

	@bet_spread.setter
	def bet_spread(self, value):
		self._bet_spread = value
