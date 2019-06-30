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
			print(f'{self.name} hits.')
		card = self.shoe.draw()
		self.hand.append(card)
		self.evaluate(card)
		return card


	def stand(self):
		print(f'{self.name} stands.')


	def score_formatted(self):
		if type(self.score) is list:
			return '/'.join([str(x) for x in self.score])
		else:
			return self.score


	def hand_formatted(self):
		return ', '.join(self.hand)


	def log_hand(self):
		print(f'{self.name} hand: {self.hand_formatted()} -> {self.score_formatted()}')


	def check_if_busted(self):
		self.busted = self.max_score > 21
		if self.busted:
			print(f'{self.name} busts!')
		return self.busted


	@property
	def max_score(self):
		if type(self.score) is int:
			return self.score
		else:
			return max(self.score)

	@property
	def name(self):
		return self.__class__.__name__

class Dealer(Person):
	def __init__(self, stand_on_soft_17=True, **kwargs):
		Person.__init__(self, **kwargs)
		self._stand_on_soft_17 = stand_on_soft_17


	@staticmethod
	def deal(person, num_of_cards=1):
		for x in range(num_of_cards):
			person.hit()


	def move(self):
		if self.check_continuation():
			self.hit()
			self.log_hand()
			self.check_next_choice()
		else:
			self.stand()


	def check_continuation(self):
		if self.stand_on_soft_17 or type(self.score) is int:
			return self.max_score < 17
		else:
			return self.max_score <= 17


	def check_next_choice(self):
		busted = self.check_if_busted()
		if not busted:
			self.move()


	def compare_people(self, persons):
		self.check_if_busted()
		for person in persons:
			if not isinstance(person, self.__class__):
				self.compare_to_dealer(person)


	def compare_to_dealer(self, person):
		player_bust = person.check_if_busted()
		if not player_bust:
			if self.busted or person.max_score > self.max_score:
				person.win()
			elif person.max_score == self.max_score:
				person.draw()
			else:
				person.lose()
		else:
			person.lose()


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
		self._bet = 0
		self._bet_spread = bet_spread


	def make_a_bet(self):
		self.log_bankroll()
		if self.use_basic_strategy:
			self.true_count_bet()
		else:
			if self.bet == 0 or self.check_new_bet():
				self.manual_bet()
		print(f'Player bets: ${self.bet}')


	def log_bankroll(self):
		print(f'Bankroll: ${self.bankroll}')


	@staticmethod
	def check_new_bet():
		choices = ['', 'y', 'ys', 'yes', 'n', 'no']
		new_bet = '"'
		while new_bet not in choices:
			print('New bet?', end='')
			new_bet = input().lower().strip()
		return new_bet in choices[:-2]


	def true_count_bet(self):
		tc = self.true_count
		if tc > 1:
			self.bet = self.bet_unit * self.true_count
		else:
			self.bet = self.bet_unit


	def manual_bet(self):
		self.bet = Player.input_bet()


	@staticmethod
	def input_bet():
		bet = 0
		while bet < 5:
			print('Make a bet: $', end='')
			bet = int(input())
		return bet


	def move(self):
		if self.use_basic_strategy:
			self.basic_strategy_move()
		else:
			move_choice = self.manual_move()
		self.evaluate_move(move_choice)


	def basic_strategy_move(self):
		pass


	@staticmethod
	def manual_move():
		move_choice = ''
		while move_choice not in ['h', 's']: # 'd', 'p'
			print('Make a move (h -> hit, s -> stand): ', end='') # , d -> double, p -> splitil
			move_choice = input().lower().strip()
		return move_choice


	def evaluate_move(self, move_choice):
		if move_choice == 'h':
			self.hit()
		elif move_choice == 's':
			self.stand()
		elif move_choice == 'd':
			self.double()
		elif move_choice == 'p':
			self.split()

	def hit(self):
		card = super().hit()
		self.count = [card, self.shoe.size]
		if len(self.hand) > 2:
			self.post_voluntary_hit()

	def post_voluntary_hit(self):
		self.log_hand()
		if self.check_if_busted():
			self.lose()
		else:
			self.move()


	def double(self):
		pass


	def split(self):
		pass


	def win(self):
		# print(f'Player wins ${self.bet}!')
		self.end_round(result='wins', difference=self.bet)
		# self.bankroll_increment = self.bet
		# self.log_bankroll()


	def lose(self):
		# print(f'Player loses ${self.bet}!')
		self.end_round(result='loses', difference=-self.bet)
		# self.bankroll_increment = -self.bet
		# self.log_bankroll()


	def end_round(self, result='draw', difference=0):
		self.bankroll_increment = difference
		difference = f"{'-' if difference < 0 else '+'}${abs(difference)}"
		print(f'Player {result}! {difference}')
		self.log_bankroll()


	def draw(self):
		print('Draw.')


	@property
	def bet(self):
		return self._bet

	@bet.setter
	def bet(self, value):
		if type(value) in [int,float]:
			self._bet = value
		else:
			raise ValueError('Bet must be int or float.')

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
