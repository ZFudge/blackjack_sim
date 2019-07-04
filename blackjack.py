from player import Player, Dealer

from inputs import ask_for_another_round

class Blackjack():
	def __init__(self, use_basic_strategy=False, stand_on_soft_17=True, num_players=1):
		self.dealer = Dealer(stand_on_soft_17=stand_on_soft_17)
		self.players = []
		for x in range(num_players):
			self.players.append(Player(use_basic_strategy=use_basic_strategy, name=x+1))
			if x == 0 and use_basic_strategy is False:
				use_basic_strategy = True


	def game(self):
		self.bets()
		self.initial_deal()
		self.log_hands()
		self.make_moves()
		self.dealer.compare_people(self.get_no_bust_players())
		return self.next_round_check()


	def bets(self):
		for player in self.players:
			player.make_a_bet()


	def initial_deal(self):
		self.dealer.hit()
		for player in self.players:
			player.hit(num_hits=2)


	def log_hands(self):
		self.dealer.log_hand()
		for person in self.players:
			person.log_hand()


	def make_moves(self):
		for player in self.non_bankrupt_players():
			player.move()
		if self.all_players_bust() is False:
			self.dealer.move()
		else:
			self.dealer.discard()


	def non_bankrupt_players(self):
		return filter(lambda player: player.bankroll > 0, self.players)


	def all_players_bust(self):
		busts = [player.busts for player in self.players]
		return all(busts)


	def get_no_bust_players(self):
		return filter(lambda player: not player.busts, self.players)


	def next_round_check(self):
		if not self.players_broke() and (self.players[0].use_basic_strategy or self.manual_round_check()):
			self.new_round()
			return True


	def players_broke(self):
		broke = [player.bankroll == 0 for player in self.players]
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
			player.new_hand()


def main():
	bkjk = Blackjack()
	while bkjk.game():
		continue

if __name__ == '__main__':
	main()
