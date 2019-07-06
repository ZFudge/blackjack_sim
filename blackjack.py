from player import Player, Dealer
from inputs import ask_for_another_round

from time import sleep

class Blackjack():
	def __init__(
			self,
			use_basic_strategy=False,
			stand_on_soft_17=True,
			num_players=1,
			can_double=True,
			can_double_after_split=True,
			can_surrender=True
			):
		self.dealer = Dealer(stand_on_soft_17=stand_on_soft_17)
		self.players = []
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
		self.bets()
		self.initial_deal()
		self.log_hands()
		self.make_moves()
		self.dealer.compare_players(self.get_no_bust_unsurrendered_players())
		return self.next_round_check()


	def bets(self):
		for player in self.players:
			player.make_a_bet()


	def initial_deal(self):
		dealer_upcard = self.dealer.hit()
		for player in self.players:
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
		return filter(lambda player: player.bankroll > 0, self.players)


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
			self.players
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
		self.dealer.new_hand()
		for player in self.players:
			player.new_hand(hard=True)


def main():
	bkjk = Blackjack(use_basic_strategy=True)
	while bkjk.game():
		sleep(0.2)
		continue

if __name__ == '__main__':
	main()
