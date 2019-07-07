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
			penetration_percentage,
			number_of_decks,
			use_basic_strategy,
			stand_on_soft_17=True,
			can_double=True,
			can_double_after_split=True,
			can_surrender=True,
			num_players=1
			):
		self.players = []
		self.y_axis_average = []
		for x in range(num_players):
			self.players.append(
				Player(
					bankroll=bankroll,
					bet_unit=bet_unit,
					bet_spread=bet_spread,
					use_basic_strategy=use_basic_strategy,
					stand_on_soft_17=stand_on_soft_17,
					can_double=True,
					can_double_after_split=True,
					can_surrender=True,
					name=x+1
					)
				)
			if x == 0 and use_basic_strategy is False:
				use_basic_strategy = True

		self.dealer = Dealer(
			stand_on_soft_17=stand_on_soft_17,
			penetration_percentage=penetration_percentage,
			number_of_decks=number_of_decks,
			# player_1=self.players[0]
			)


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


	def game(self):
		if self.non_bankrupt_players():
			self.bets()
			self.initial_deal()
			self.log_hands()
			self.make_moves()
			self.dealer.compare_players(self.get_no_bust_unsurrendered_players())
			self.next_round_check()
		self.update_axes()
		print(self.dealer.shoe.shoe)


def main(
	bankroll,
	bet_unit,
	bet_spread,
	use_basic_strategy,
	penetration_percentage,
	number_of_decks,
	stand_on_soft_17,
	can_double,
	can_double_after_split,
	can_surrender,
	num_players,
	game_interval,
	speed_ms
	):
	bkjk = Blackjack(
		bankroll=bankroll,
		bet_unit=bet_unit,
		bet_spread=bet_spread,
		use_basic_strategy=use_basic_strategy,
		num_players=num_players,
		penetration_percentage=penetration_percentage,
		number_of_decks=number_of_decks
		)

	plot.style.use('fast')

	# fig1, ax1 = plot.subplots(1,1)
	# fig2, ax2 = plot.subplots()

	fig, (ax1, ax2) = plot.subplots(1, 2, figsize=(15, 7))
	# fig.

	plyr = bkjk.players[0]
	x_axis = []
	x = count()
	x_axis.append(next(x))
	bkjk.average()
	colors = ['#0077dd', '#dd0022']
	def cont():
		while len(bkjk.non_bankrupt_players()) > 0:
			yield True

	def progress_rounds():
		for y in range(game_interval):
			x_axis.append(next(x))
			bkjk.game()
			bkjk.average()

	def animation1(n):
		ax1.cla()

		progress_rounds()

		for player in bkjk.players:
			print(f'	plotting {player.name} - x:{len(x_axis)}, y:{len(player.y_axis)}')
			ax1.plot(x_axis, player.y_axis, label=player.name)

		print(f'	plotting average - x:{len(x_axis)}, y:{len(bkjk.y_axis_average)}', end='')
		ax1.plot(x_axis, bkjk.y_axis_average, linestyle='--', label='Average')
		ax1.legend(loc='upper left')
		ax1.set_xlabel('Hands')
		ax1.set_ylabel('Bankroll - USD')
		ax1.set_title(f'Blackjack Simulation - p:{penetration_percentage}%, #d:{number_of_decks}, ibr:${bankroll}, u: ${bet_unit}, sp:{bet_spread}')
		ax1.grid(True)
		plot.tight_layout()


	def animation2(m):
		ax2.cla()
		print(f'	plotting pie - {len(x_axis) * len(bkjk.non_bankrupt_players()) - bkjk.players[0].wins}, {bkjk.players[0].wins}', end='')
		labels = ['Wins', 'Losses']
		ax2.pie(
			[ plyr.wins, plyr.losses ],
			labels=labels,
			autopct='%1.1f%%',
			# shadow=True,
			startangle=90,
			wedgeprops={"edgecolor":"k"},
			colors=colors
			)

		plot.tight_layout()

	# animate = FuncAnimation(plot.gcf(), animation, frames=cont, interval=speed_ms, repeat=False)

	animate1 = FuncAnimation(plot.gcf(), animation1, frames=cont, interval=speed_ms, repeat=False)
	animate2 = FuncAnimation(plot.gcf(), animation2, frames=cont, interval=speed_ms, repeat=False)

	plot.show()


if __name__ == '__main__':
	main(
		bankroll=10000,
		bet_unit=150,
		bet_spread=30,
		use_basic_strategy=True,
		penetration_percentage=70,
		number_of_decks=8,
		stand_on_soft_17=True,
		can_double=True,
		can_double_after_split=True,
		can_surrender=True,
		num_players=6,
		game_interval=15,
		speed_ms=200
		)

