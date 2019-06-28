from basic_strategy import Basic_Strategy
from evaluate import Evaluate
from hi_lo import Hi_Lo
from shoe import Shoe

shoe = Shoe()

class Person(Evaluate):
	def __init__(self):
		self.shoe = shoe
		self.hand = []
		self.score = 0
		self.busted = False


	def new_hand(self):
		self.hand = []
		self.score = 0
		self.busted = False


	def evaluate(self, card):
		card = card[0]
		self.score = self.evaluate_card_value(
			score=self.score,
			card=card,
			)


	def hit(self):
		if len(self.hand) > 2:
			print(f'{self.__class__.__name__} hits.')
		card = self.shoe.draw()
		self.hand.append(card)
		self.evaluate(card)
		return card


	def stand(self):
		print(f'{self.__class__.__name__} stands.')

	def score_formatted(self):
		# print(self.score)
		if type(self.score) is list:
			return '/'.join([str(x) for x in self.score])
		else:
			return self.score

	def hand_formatted(self):
		return ', '.join(self.hand)

	def log_hand(self):
		print(f'{self.__class__.__name__} hand: {self.hand_formatted()} -> {self.score_formatted()}')

	@property
	def max_score(self):
		if type(self.score) is int:
			return self.score
		else:
			return max(self.score)

	def check_if_busted(self):
		bust = self.max_score > 21
		if bust:
			self.busted = True
			print(f'{self.__class__.__name__} busts!')
		return bust


class Dealer(Person):
	def __init__(self, stand_on_soft_17=True, **kwargs):
		Person.__init__(self, **kwargs)
		self._stand_on_soft_17 = stand_on_soft_17


	def deal(self, person, num_of_cards=1):
		for x in range(num_of_cards):
			person.hit()

	def move(self):
		if self.max_score < 17 or (self.max_score == 17 and not self.stand_on_soft_17):
			self.hit()
			self.log_hand()
		else:
			self.stand()


	def compare(self, persons):
		self.check_if_busted()
		dealer_bust = self.busted
		for person in persons:
			if not isinstance(person, self.__class__):
				if dealer_bust or person.max_score > self.max_score:
					person.win()
				elif person.max_score == self.max_score:
					person.draw()
				else:
					person.lose()
				# person.log_hand()


	@property
	def stand_on_soft_17(self):
		return self._stand_on_soft_17


class Player(Person, Hi_Lo):
	def __init__(self, use_basic_strategy=False, bankroll=1000, bet_unit=5, bet_spread=12, **kwargs):
		Person.__init__(self, **kwargs)
		Hi_Lo.__init__(self)
		self._use_basic_strategy = use_basic_strategy
		self._bankroll = bankroll
		self._bet_unit = bet_unit
		self._bet = bet_unit
		self._bet_spread = bet_spread


	def move(self):
		if self.use_basic_strategy:
			pass
		else:
			print('Make a move: h -> hit, s -> stand') # , d -> double, p -> split
			move_choice = self.get_choice()
		self.evaluate_move(move_choice)


	def get_choice(self):
		move_choice = ''
		while move_choice not in ['h', 's']: # 'd', 'p'
			move_choice = input().lower().strip()
		return move_choice


	def evaluate_move(self, move_choice):
		if move_choice == 'h':
			self.hit()
			self.log_hand()
			if self.check_if_busted():
				self.lose()
			else:
				self.move()
		elif move_choice == 's':
			self.stand()
		elif move_choice == 'd':
			self.double()
		elif move_choice == 'p':
			self.split()


	def double(self):
		pass


	def split(self):
		pass

	# def log_hand(self):
	# 	super().log_hand()
	# 	if len(self.hand) == 2:
	# 		print(f'Current bet: ${self.bet}, Bankroll: ${self.bankroll}')

	def end_round(self, result='draw', difference=0):
		print(f'Player {result}')
		self.bankroll_increment = difference

	def win(self):
		print(f'Player wins ${self.bet}!')
		self.bankroll_increment = self.bet_unit

	def draw(self):
		print('Draw.')

	def lose(self):
		print(f'Player loses ${self.bet}!')
		self.bankroll_increment = -self.bet_unit

	def make_a_bet(self):
		print(f'Bankroll: ${self.bankroll}')
		if self.use_basic_strategy:
			tc = self.true_count
			if tc > 1:
				self._bet = self.bet_unit * self.true_count
			else:
				self._bet = self.bet_unit
		else:
			print('Make a bet')
			new_bet = input()
		print(f'Player bets: ${self._bet}')

	@property
	def bet(self):
		return self._bet

	@bet.setter
	def bet(self, value):
		if type(value) in [int, float]:
			self._bet = value
		else:
			raise ValueError('Bet must be int or float.')

	def hit(self):
		card = super().hit()
		self.count = [card, self.shoe.size]


	@property
	def use_basic_strategy(self):
		return self._use_basic_strategy

	@property
	def bankroll(self):
		return self._bankroll

	@bankroll.setter
	def bankroll_increment(self, value):
		if type(value) in [int, float]:
			self._bankroll += value
		else:
			raise ValueError('Changes to bankroll must be int or float.')

	@property
	def bet_unit(self):
		return self._bet_unit

	@bet_unit.setter
	def bet_unit(self, value):
		if isinstance(value, int):
			self._bet_unit = value
		else:
			raise ValueError('Betting unit must be int.')

	@property
	def bet_spread(self):
		return self._bet_spread

	@bet_spread.setter
	def bet_spread(self, value):
		if isinstance(value, int):
			self._bet_spread = value
		else:
			raise ValueError('Bet spread must be int.')


def main():
	pass

if __name__ == '__main__':
	main()
