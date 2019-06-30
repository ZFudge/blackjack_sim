import re

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
		if len(self.hand) > 2:
			print(f'{self.name} hits.')
		card = self.shoe.draw()
		self.hand.append(card)
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
		if self.blackjack:
			return


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
			raise ValueError('Busts value must be boolean')

	@property
	def blackjack(self):
		return self._blackjack

	@blackjack.setter
	def blackjack(self, value):
		if type(value) is bool:
			self._blackjack = value
		else:
			raise ValueError('Blackjack value must be boolean')

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
		super().move()
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
			if not isinstance(person, self.__class__):
				if not person.busts:
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
		self._bet_spread = bet_spread
		self._bet = 0
		self._double = False


	def make_a_bet(self):
		self.log_bankroll()
		if self.use_basic_strategy:
			self.true_count_bet()
		else:
			if self.bet == 0 or not self.check_same_bet():
				self.manual_bet()
		print(f'Player bets: ${self.bet}')


	def log_bankroll(self):
		print(f'Bankroll: ${self.bankroll}')


	@staticmethod
	def check_same_bet():
		choices = ['', 'y', 'ys', 'yes', 'n', 'no']
		new_bet = '"'
		while new_bet not in choices:
			print('Same bet?: ', end='')
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
			bet = re.sub('[^0-9]','', input())
			if len(bet) == 0:
				bet = 0
			else:
				bet = int(bet)
		return bet


	def move(self):
		super().move()
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
			self.double = True
			self.hit()
		elif move_choice == 'p':
			self.split()


	def hit(self):
		card = super().hit()
		self.count = [card, self.shoe.size]
		if len(self.hand) > 2:
			self.post_voluntary_hit()


	def new_hand(self):
		super().new_hand()
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
	def double(self):
		return self._double

	@double.setter
	def double(self, value):
		if type(value) is bool:
			self._double = value
		else:
			raise ValueError('Double value must be a boolean')

	@property
	def bet(self):
		return self._bet

	@bet.setter
	def bet(self, value):
		if type(value) in [int,float]:
			self._bet = value
		else:
			raise ValueError('Bet value must be int or float')

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
			raise ValueError('Bankroll increment value must be int or float')

	@property
	def bet_unit(self):
		return self._bet_unit

	@bet_unit.setter
	def bet_unit(self, value):
		if isinstance(value, int):
			self._bet_unit = value
		else:
			raise ValueError('Betting unit value must be int')

	@property
	def bet_spread(self):
		return self._bet_spread

	@bet_spread.setter
	def bet_spread(self, value):
		if isinstance(value, int):
			self._bet_spread = value
		else:
			raise ValueError('Bet spread value must be int')


def main():
	pass

if __name__ == '__main__':
	main()
