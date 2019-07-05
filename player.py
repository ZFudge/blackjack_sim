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
		if len(self.hand) > 2:
			print(f'{self.name} hits. ', end='')
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


	def compare_players(self, players):
		if not self.busts:
			self.check_if_busted()
		for player in players:
			self.compare_to_dealer(player)
			if player.split_results:
				for result in player.split_results:
					player.revisit_split(result)
					self.compare_to_dealer(player)


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
		self._surrendered = False
		self.split_hands = []
		self.split_results = []


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
		if blackjack is False and self.double is False:
			if self.use_basic_strategy:
				self.basic_strategy_move()
			else:
				move_choice = manual_move(self.available_moves())
			self.evaluate_move(move_choice)
			if self.split_hands:
				self.iterate_splits()


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
		elif move_choice == 'r':
			self.surrender()


	def hit(self, num_hits=1):
		card = super().hit()
		self.count = [card, self.shoe.size]
		if len(self.hand) > 2:
			self.post_voluntary_hit()
		if num_hits > 1:
			self.hit(num_hits-1)


	def new_hand(self, hard=False):
		super().new_hand()
		if self.double:
			self.double = False
		if self.surrendered:
			self.surrendered = False
		if hard:
			self.split_results = []


	def post_voluntary_hit(self):
		self.log_hand()
		if self.check_if_busted():
			self.lose()
		else:
			self.move()


	def split(self):
		print(f'{self.name} splits!')
		self.split_hands.append(self.hand.pop())
		self.split_score()
		self.hit()
		self.log_hand()
		self.move()


	def split_score(self):
		if type(self.score) is list:
			self.score = [1, 11]
		else:
			self.score = int(self.score / 2)


	def can_split(self):
		return self.hand[0][0] == self.hand[1][0]


	def split_record(self):
		result =  {
			'score': self.score,
			# 'double': self.double,
			'bet': self.bet,
			'busts': self.busts
		}
		self.split_results.append(result)
		print(f"Previous split score: {result['score']}, bet: {result['bet']}")


	def log_hand(self):
		super().log_hand()
		if self.split_hands:
			print(f'Splits: {self.split_hands}')


	def iterate_splits(self):
		print(f'Iterating {len(self.split_hands)} split(s).')
		self.split_record()
		self.new_hand()
		card = self.split_hands.pop()
		self.hand.append(card)
		self.evaluate(card)
		self.hit()
		self.log_hand()
		self.move()


	def revisit_split(self, results):
		self.score = results['score']
		self.bet = results['bet']
		self.busts = results['busts']


	def no_splits(self):
		if not self.split_results:
			return True


	def valid_splits(self):
		valids = [ x['busts'] is False for x in self.split_results]
		return any(valids)


	def win(self):
		self.end_round(result='wins', difference=self.bet)


	def lose(self):
		self.end_round(result='loses', difference=-self.bet)


	def surrender(self):
		self.surrendered = True
		self.end_round(result='surrenders', difference=self.bet / -2)


	def end_round(self, result, difference=0):
		self.bankroll_increment = difference
		difference = f"{'-' if difference < 0 else '+'}${abs(difference)}"
		print(f'  {self.name} {result}! {difference}')
		self.log_bankroll()


	def draw(self):
		print('Push.')
		self.log_bankroll()


	def available_moves(self):
		moves = ['[h]it', '[s]tand']
		double = '[d]ouble'
		split = 's[p]lit'
		surrender = 'su[r]render'

		if len(self.hand) == 2:
			moves.append(surrender)
			if self.can_double():
				moves.append(double)
			if self.can_split():
				moves.append(split)
		return  {
			'short': [move[move.index('[')+1][0:] for move in moves],
			'long': ', '.join(moves)
		}


	def can_double(self):
		return self.bet * 2 <= self.bankroll


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
				self.bet *= 2
				print(f'{self.name} doubles: ${self.bet}')
			else:
				self.bet /= 2
		else:
			raise ValueError(f'Double value must be a boolean. Received {type(value)}')

	@property
	def surrendered(self):
		return self._surrendered

	@surrendered.setter
	def surrendered(self, value):
		if type(value) is bool:
			self._surrendered = value
		else:
			raise ValueError(f'Surrender value must be a boolean. Received {type(value)}')


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
