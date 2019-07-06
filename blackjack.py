from player import Player, Dealer
from inputs import ask_for_another_round

from time import sleep
from itertools import count
import sys

import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation


class Blackjack():
	def __init__(
			self,
			bankroll,
			bet_unit,
			bet_spread,
			use_basic_strategy=False,
			stand_on_soft_17=True,
			num_players=1,
			can_double=True,
			can_double_after_split=True,
			can_surrender=True
			):
		self.dealer = Dealer(stand_on_soft_17=stand_on_soft_17)
		self.players = []
		self.y_axis_average = []
		for x in range(num_players):
			self.players.append(
				Player(
					use_basic_strategy=use_basic_strategy,
					name=x+1,
					stand_on_soft_17=stand_on_soft_17,
					can_double=True,
					can_double_after_split=True,
					can_surrender=True
					)
				)
			if x == 0 and use_basic_strategy is False:
				use_basic_strategy = True


	def game(self):
		if self.non_bankrupt_players():
			self.bets()
			self.initial_deal()
			self.log_hands()
			self.make_moves()
			self.dealer.compare_players(self.get_no_bust_unsurrendered_players())
			self.update_axes()
			return self.next_round_check()


	def bets(self):
		for player in self.players:
			if not player.bankrupt:
				player.make_a_bet()


	def initial_deal(self):
		dealer_upcard = self.dealer.hit()
		for player in self.players:
			if not player.bankrupt:
				player.dealer_upcard = dealer_upcard
				player.hit()


	def log_hands(self):
		self.dealer.log_hand()
		for person in self.players:
			person.log_hand()


	def make_moves(self):
		for player in self.non_bankrupt_players():
			player.move()
		if (not self.all_players_bust() and not self.all_players_surrender()) or self.valid_splits_present():
			self.dealer.move()
		else:
			self.dealer.reveal_card()


	def non_bankrupt_players(self):
		return list(filter(lambda player: player.bankrupt is False, self.players))


	def all_players_bust(self):
		busts = [player.busts for player in self.players]
		return all(busts)


	def all_players_surrender(self):
		surrenders = [player.surrendered for player in self.players]
		return all(surrenders)

	def valid_splits_present(self):
		valids = []
		for player in self.players:
			valids.append(player.valid_splits())
		return any(valids)


	def get_no_bust_unsurrendered_players(self):
		return filter(
			lambda player: (player.busts is False and player.surrendered is False) or player.valid_splits(),
			self.non_bankrupt_players()
			)


	def next_round_check(self):
		if not self.players_broke() and (self.players[0].use_basic_strategy or self.manual_round_check()):
			self.new_round()
			return True


	def players_broke(self):
		broke = [player.bankroll < 1 for player in self.players]
		return all(broke)


	def manual_round_check(self):
		answer = ask_for_another_round()
		if answer.startswith('y') or answer == '':
			return True
		else:
			print('Bye.')


	def new_round(self):
		print('New round')
		self.dealer.new_hand()
		for player in self.players:
			player.new_hand(hard=True)


	def average(self):
		average = round(sum([ player.bankroll for player in self.players]) / len(self.players))
		self.y_axis_average.append(average)


	def update_axes(self):
		for player in self.players:
			player.update_y_axis()


def main():
	bkjk = Blackjack(
		bankroll=1000,
		bet_unit=10,
		bet_spread=20,
		use_basic_strategy=True,
		num_players=6
		)

	# plot.style.use()
	x_axis = []
	x = count()

	def cont():
		while len(bkjk.non_bankrupt_players()) > 0:
			yield True

	def animation(n):
		x_axis.append(next(x))
		plot.cla()
		for player in bkjk.players:
			plot.plot(x_axis, player.y_axis, label=player.name)
		bkjk.average()
		plot.plot(x_axis, bkjk.y_axis_average, linestyle='--', label='Player Average')

		plot.xlabel('Hands')
		plot.ylabel('Bankroll - USD')
		plot.title('Blackjack Simulation')
		plot.legend(loc='upper left')
		plot.grid(True)
		plot.tight_layout()
		bkjk.game()

	animate = FuncAnimation(plot.gcf(), animation, frames=cont, interval=212, repeat=False)
	plot.show()


if __name__ == '__main__':
	main()
