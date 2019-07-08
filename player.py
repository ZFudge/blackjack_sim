from basic_strategy import Basic_Strategy
from evaluate import Evaluate
from hi_lo import Hi_Lo
from shoe import Shoe

from inputs import check_same_bet, input_bet, manual_move

from decimal import Decimal

hl = Hi_Lo()
shoe = Shoe(hl)

class Person(Evaluate):
	def __init__(self):
		self.hl = hl
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
		self.hl.count_card([card, self.shoe.size])
		self.hand.append(card)
		if len(self.hand) > 2:
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
		if self.max_score == 21 and len(self.hand) == 2:
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
			raise ValueError(f'Busts value must be boolean. Received {type(value)}, {value}')

	@property
	def blackjack(self):
		return self._blackjack

	@blackjack.setter
	def blackjack(self, value):
		if type(value) is bool:
			self._blackjack = value
		else:
			raise ValueError(f'Blackjack value must be boolean. Received {type(value)}, {value}')

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
	def __init__(self, stand_on_soft_17=True, penetration_percentage=65, number_of_decks=8):
		Person.__init__(self)
		self._stand_on_soft_17 = stand_on_soft_17
		self._hidden_card = None
		self.shoe.penetration_percentage=penetration_percentage
		self.shoe.number_of_decks=number_of_decks


	def move(self):
		blackjack = super().move()
		if self.hidden_card:
			self.reveal_card()
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
					if result['busts'] is False:
						player.revisit_split(result)
						self.compare_to_dealer(player)


	def compare_to_dealer(self, player):
		if not player.busts:
			player_bust = player.check_if_busted()
		if not player.busts:
			if self.busts or player.max_score > self.max_score:
				player.win()
			elif player.max_score == self.max_score:
				player.draw()
			else:
				player.lose()
		else:
			pass
			# player.lose()


	def reveal_card(self):
		card = self.hidden_card
		self.hl.count_card((card, self.shoe.size))
		self.hidden_card = None
		self.hand.append(card)
		self.evaluate(card)
		self.log_hand()


	def hand_formatted(self):
		if len(self.hand) == 1:
			return ', '.join(self.hand + ['*'])
		return ', '.join(self.hand)


	def new_hand(self, hard=False):
		super().new_hand()
		self.hidden_card = None


	def hit(self):
		card = super().hit()
		if len(self.hand) == 1:
			self.hidden_hit()
		return card


	def hidden_hit(self):
		card = self.shoe.draw()
		self.hidden_card = card


	@property
	def stand_on_soft_17(self):
		return self._stand_on_soft_17

	@property
	def hidden_card(self):
		return self._hidden_card

	@hidden_card.setter
	def hidden_card(self, value):
		if value is None or (type(value) is str and len(value) == 2):
			self._hidden_card = value



class Player(Person, Basic_Strategy):
	wins = 0
	losses = 0

	def __init__(
			self,
			name,
			stand_on_soft_17,
			can_double,
			can_double_after_split,
			can_surrender,
			use_basic_strategy=False,
			bankroll=1000,
			bet_unit=5,
			bet_spread=12,
			**kwargs
			):
		Person.__init__(self)
		Basic_Strategy.__init__(self, stand_on_soft_17)
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
		self.y_axis = [bankroll]
		self._dealer_upcard = None
		self._can_double = can_double
		self._can_double_after_split = can_double_after_split
		self._can_surrender = can_surrender


	def make_a_bet(self):
		self.log_bankroll()
		self.check_bet_adjustment()
		if self.use_basic_strategy:
			self.true_count_bet()
		else:
			if self.bet == 0 or self.bet_beneath_threshold() or not check_same_bet():
				self.manual_bet()
		print(f'{self.name} bets: ${self.bet}')


	def log_bankroll(self):
		print(f'{self.name} bankroll: ${self.bankroll}')


	def bet_beneath_threshold(self):
		return self.bet > self.bankroll


	def true_count_bet(self):
		tc_vetti = self.hl.true_count - 1
		if tc_vetti > 1:
			tc_bet = self.bet_unit * tc_vetti
			if self.bet_spread is not None:
				if tc_bet > self.bet_spread:
					if self.bet_spread > self.bankroll:
						self.bet = self.bankroll
					else:
						self.bet = self.bet_spread
				else:
					if tc_bet > self.bankroll:
						self.bet = self.bankroll
					else:
						self.bet = tc_bet
			elif tc_bet > self.bankroll:
				self.bet = self.bankroll
			else:
				self.bet = tc_bet
		else:
			self.bet = self.bet_unit


	def manual_bet(self):
		self.bet = input_bet(self.bankroll)


	def move(self):
		blackjack = super().move()
		if blackjack is False and self.double is False:
			if self.use_basic_strategy:
				move_choice = self.basic_strategy_move()
			else:
				move_choice = manual_move(self.available_moves())
			self.evaluate_move(move_choice)
			if self.split_hands:
				self.iterate_splits()


	def basic_strategy_move(self):
		soft = self.all_lists([self.score])
		dealer_upcard = self.dealer_upcard
		if type(dealer_upcard) is list:
			dealer_upcard = 11
		move = None
		if self.can_split():
			if soft:
				move = self.strategy_map['split']['A'][dealer_upcard - 2]
			else:
				move = self.strategy_map['split'][self.score / 2][dealer_upcard - 2]
				if move == 'ns':
					move = None
		if move is None:
			if soft:
				move = self.strategy_map['soft'][self.max_score][dealer_upcard - 2] 
			else:
				move = self.strategy_map['hard'][self.score][dealer_upcard - 2]
		print(f'Move: {move}')
		return move


	def evaluate_move(self, move_choice):
		if move_choice == 's':
			self.stand()
		elif move_choice == 'h':
			self.hit()
		elif move_choice in ['ds', 'dh', 'd', 'h', '']:
			if move_choice in ['ds', 'dh', 'd'] and self.can_double:
				self.double = True
			elif move_choice == 'ds':
				self.stand()
				return
			self.hit()
		elif move_choice == 'p':
			self.split()
		elif move_choice == 'ph':
			if self.can_double_after_split:
				self.split()
			else:
				self.hit()
		elif move_choice in ['r', 'rh']:
			if self.can_surrender:
				self.surrender()
			else:
				self.hit()


	def hit(self):
		card = super().hit()
		hand_length = len(self.hand)
		if hand_length > 2:
			self.post_voluntary_hit()
		if hand_length == 1:
			self.hit()


	def new_hand(self, hard=False):
		super().new_hand()
		if self.double:
			self.double = False
		if self.surrendered:
			self.surrendered = False
		if hard:
			self.split_results = []
			self.dealer_upcard = None


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
		return len(self.hand) == 2 and self.hand[0][0] == self.hand[1][0]


	def split_record(self):
		result =  {
			'score': self.score,
			'double': self.double,
			'bet': self.bet,
			'busts': self.busts
		}
		self.split_results.append(result)
		print(f" Recording split. (Score: {self.score_formatted()}, Bet: {self.bet}, Busts: {self.busts}, Double: {self.double})")


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
		self.busts = results['busts']
		self.double = results['double']
		self.bet = results['bet']
		print(f' Revisiting split. (Score: {self.score_formatted()}, Bet: {self.bet}, Busts: {self.busts}, Double: {self.double}')


	def no_splits(self):
		if not self.split_results:
			return True


	def valid_splits(self):
		valids = [ x['busts'] is False for x in self.split_results]
		return any(valids)

	def update_y_axis(self):
		self.y_axis.append(round(self.bankroll))

	def win(self):
		Player.wins += 1
		if self.blackjack:
			self.end_round(result='wins', difference=self.bet * 15/10)
		else:
			self.end_round(result='wins', difference=self.bet)


	def lose(self):
		Player.losses += 1
		self.end_round(result='loses', difference=-self.bet)


	def surrender(self):
		self.surrendered = True
		self.end_round(result='surrenders', difference=self.bet / -2)


	def end_round(self, result, difference=0):
		self.bankroll_increment = difference
		difference = f"{'-' if difference < 0 else '+'}${abs(difference)}{' ~ D' if self.double else ''}"
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
			if self.can_surrender:
				moves.append(surrender)
			if self.can_double:
				moves.append(double)
			if self.can_split():
				moves.append(split)
		return  {
			'short': [move[move.index('[')+1][0:] for move in moves],
			'long': ', '.join(moves)
		}

	@property
	def bankrupt(self):
		return self.bankroll < 1

	@property
	def can_double(self):
		return self._can_double and self.bet * 2 <= self.bankroll

	@property
	def can_double_after_split(self):
		return self._can_double_after_split

	@property
	def can_surrender(self):
		return self._can_surrender and len(self.hand) == 2

	@property
	def dealer_upcard(self):
		return self._dealer_upcard

	@dealer_upcard.setter
	def dealer_upcard(self, value):
		if value is None:
			self._dealer_upcard = None
		elif type(value) in [str, list] and len(value) == 2:
			self._dealer_upcard = self.get_value(value[0])
		else:
			raise ValueError(f'Dealer upcard value must be string, two characters/items in length. Received {type(value)}, {value}')

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
			raise ValueError(f'Double value must be a boolean. Received {type(value)}, {value}')

	@property
	def surrendered(self):
		return self._surrendered

	@surrendered.setter
	def surrendered(self, value):
		if type(value) is bool:
			self._surrendered = value
		else:
			raise ValueError(f'Surrender value must be a boolean. Received {type(value)}, {value}')

	@property
	def bet(self):
		return round(self._bet, 2)

	@bet.setter
	def bet(self, value):
		if type(value) in [int, float, Decimal]:
			self._bet = Decimal(value)
		else:
			raise ValueError(f'Bet value must be int, float, or Decimal. Received {type(value)}, {value}')

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
			raise ValueError(f'Bankroll increment value must be Decimal. Received {type(value)}, {value}')

	@property
	def bet_unit(self):
		return self._bet_unit

	@bet_unit.setter
	def bet_unit(self, value):
		if isinstance(value, int):
			self._bet_unit = value
		else:
			raise ValueError(f'Betting unit value must be int. Received {type(value)}, {value}')

	@property
	def bet_spread(self):
		return self._bet_spread

	@bet_spread.setter
	def bet_spread(self, value):
		if isinstance(value, int):
			self._bet_spread = value
		else:
			raise ValueError(f'Bet spread value must be int. Received {type(value)}, {value}')

	

def main():
	pass

if __name__ == '__main__':
	main()
