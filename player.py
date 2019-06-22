class Person():
	def __init__(self):
		self.score = 0
		self.hand = []

	def new_hand(self):
		self.hand = []


class Dealer(Person):
	pass


class Player(Person):
	def __init__(self, bankroll=1000, bet_unit=5, bet_spread=12):
		Person.__init__(self)
		self.bankroll = bankroll
		self.bet_unit = bet_unit
		self.bet_spread = bet_spread

