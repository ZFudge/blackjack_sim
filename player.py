from basic_strategy import Basic_Strategy
from evaluate import Evaluate
from hi_lo import Hi_Lo
from shoe import Shoe

from inputs import check_same_bet, input_bet, manual_move

from decimal import Decimal

shoe = Shoe()

class Person(Evaluate):
	def __init__(self):
		self.shoe = shoe
		self.hand = []
		self.score = 0
		self._busts = False
		self._blackjack = False


	def new_hand(self):
		self.hand = []
		self.score = 0
		self._busts = False
		self._blackjack = False


	def log_hand(self):
		print(f'{self.name} hand: {self.hand_formatted()} -> {self.score_formatted()}')


	def hit(self):
		card = self.shoe.draw()
		self.hand.append(card)
		if len(self.hand) > 2:# or (len(self.hand) == 2 and self.name.startswith('D')):
			print(f'{self.name} hits.')
		self.evaluate(card)
		return card


	def stand(self):
		print(f'{self.name} stands.')


	def evaluate(self, card):
		card = card[0]
		self.score = self.evaluate_card_value(
			score=self.score,
			card=card,
			)
		self.check_for_blackjack()


	def check_for_blackjack(self):
		if self.max_score == 21:
			self.blackjack = True
			print(f'{self.name} blackjack!')


	def check_if_busted(self):
		self.busts = self.max_score > 21
		if self.busts:
			print(f'{self.name} busts!')
		return self.busts


	def move(self):
		return self.blackjack


	def score_formatted(self):
		if type(self.score) is list:
			return '/'.join([str(x) for x in self.score])
		else:
			return self.score


	def hand_formatted(self):
		return ', '.join(self.hand)


	@property
	def busts(self):
		return self._busts

	@busts.setter
	def busts(self, value):
		if type(value) is bool:
			self._busts = value
		else:
			raise ValueError(f'Busts value must be boolean. Received {type(value)}')

	@property
	def blackjack(self):
		return self._blackjack

	@blackjack.setter
	def blackjack(self, value):
		if type(value) is bool:
			self._blackjack = value
		else:
			raise ValueError(f'Blackjack value must be boolean. Received {type(value)}')

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


	def move(self):
		blackjack = super().move()
		if blackjack is False:
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
		if not self.busts:
			self.check_if_busted()
		if not self.busts:
			self.move()


	def compare_people(self, persons):
		if not self.busts:
			self.check_if_busted()
		for person in persons:
			self.compare_to_dealer(person)


	def compare_to_dealer(self, person):
		player_bust = person.check_if_busted()
		if not player_bust:
			if self.busts or person.max_score > self.max_score:
				person.win()
			elif person.max_score == self.max_score:
				person.draw()
			else:
				person.lose()
		else:
			person.lose()


	def discard(self):
		card = self.shoe.draw()
		self.hand.append(card)
		self.evaluate(card)
		self.log_hand()


	def hand_formatted(self):
		if len(self.hand) == 1:
			return ', '.join(self.hand + ['*'])
		return ', '.join(self.hand)


	@property
	def stand_on_soft_17(self):
		return self._stand_on_soft_17


class Player(Person, Hi_Lo):
	def __init__(self, name, use_basic_strategy=False, bankroll=1000, bet_unit=5, bet_spread=12, **kwargs):
		Person.__init__(self, **kwargs)
		Hi_Lo.__init__(self)
		self._name = f'_{name}'
		self._use_basic_strategy = use_basic_strategy
		self._bankroll = Decimal(bankroll)
		self._bet_unit = bet_unit
		self._bet_spread = bet_spread
		self._bet = 0
		self._double = False


	def make_a_bet(self):
		self.log_bankroll()
		if self.use_basic_strategy:
			self.true_count_bet()
		else:
			if self.bet == 0 or self.bet_beneath_threshold() or not check_same_bet():
				self.manual_bet()
		print(f'{self.name} bets: ${self.bet}')


	def log_bankroll(self):
		print(f'Bankroll: ${self.bankroll}')


	def bet_beneath_threshold(self):
		return self.bet > self.bankroll


	def true_count_bet(self):
		tc = self.true_count
		if tc > 1:
			self.bet = self.bet_unit * self.true_count
		else:
			self.bet = self.bet_unit


	def manual_bet(self):
		self.bet = input_bet(self.bankroll)


	def move(self):
		blackjack = super().move()
		if blackjack is False:
			if self.use_basic_strategy:
				self.basic_strategy_move()
			else:
				move_choice = manual_move()
			self.evaluate_move(move_choice)


	def basic_strategy_move(self):
		pass


	def evaluate_move(self, move_choice):
		if move_choice in ['d', 'h', '']:
			if move_choice == 'd':
				self.double = True
			self.hit()
		elif move_choice == 's':
			self.stand()
		elif move_choice == 'p':
			self.split()


	def hit(self, num_hits=1):
		card = super().hit()
		self.count = [card, self.shoe.size]
		if len(self.hand) > 2:
			self.post_voluntary_hit()
		if num_hits > 1:
			self.hit(num_hits-1)


	def new_hand(self):
		super().new_hand()
		if self.double:
			self.double = False


	def post_voluntary_hit(self):
		self.log_hand()
		if self.check_if_busted():
			self.lose()
		else:
			self.move()


	def split(self):
		pass


	def win(self):
		self.end_round(result='wins', difference=self.bet)


	def lose(self):
		self.end_round(result='loses', difference=-self.bet)


	def end_round(self, result='draw', difference=0):
		self.bankroll_increment = difference
		difference = f"{'-' if difference < 0 else '+'}${abs(difference)}"
		print(f'{self.name} {result}! {difference}')
		self.log_bankroll()


	def draw(self):
		print('Draw.')


	def can_split(self):
		if len(self.hand):
			return self.hand[0] == self.hand[1]


	@property
	def name(self):
		return self.__class__.__name__ + self._name

	@property
	def double(self):
		return self._double

	@double.setter
	def double(self, value):
		if type(value) is bool:
			self._double = value
			if self._double is True:
				print(f'{self.name} doubles!')
				self.bet *= 2
			else:
				self.bet /= 2
		else:
			raise ValueError(f'Double value must be a boolean. Received {type(value)}')

	@property
	def bet(self):
		return round(self._bet, 2)

	@bet.setter
	def bet(self, value):
		if type(value) in [int, float, Decimal]:
			self._bet = Decimal(value)
		else:
			raise ValueError(f'Bet value must be int, float, or Decimal. Received {type(value)}')

	@property
	def use_basic_strategy(self):
		return self._use_basic_strategy

	@property
	def bankroll(self):
		return round(self._bankroll, 2)

	@bankroll.setter
	def bankroll_increment(self, value):
		if type(value) is Decimal:
			self._bankroll += value
		else:
			raise ValueError(f'Bankroll increment value must be Decimal. Received {type(value)}')

	@property
	def bet_unit(self):
		return self._bet_unit

	@bet_unit.setter
	def bet_unit(self, value):
		if isinstance(value, int):
			self._bet_unit = value
		else:
			raise ValueError(f'Betting unit value must be int. Received {type(value)}')

	@property
	def bet_spread(self):
		return self._bet_spread

	@bet_spread.setter
	def bet_spread(self, value):
		if isinstance(value, int):
			self._bet_spread = value
		else:
			raise ValueError(f'Bet spread value must be int. Received {type(value)}')


def main():
	pass

if __name__ == '__main__':
	main()
