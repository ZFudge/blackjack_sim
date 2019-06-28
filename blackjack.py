from player import Player, Dealer


class Blackjack():
	def __init__(self, use_basic_strategy=False, stand_on_soft_17=True):
		self.dealer = Dealer(stand_on_soft_17=stand_on_soft_17)
		self.player = Player(use_basic_strategy=use_basic_strategy)
		self.people = [self.dealer, self.player]


	def initial_deal(self):
		num_cards = 1
		for person in self.people:
			self.dealer.deal(person=person, num_of_cards=num_cards)
			num_cards += 1


	def log_hands(self):
		for person in self.people:
			person.log_hand()


	def moves(self):
		self.player.move()
		if not self.player.busted:
			self.dealer.move()


	def new_round(self):
		for person in self.people:
			person.new_hand()


	def game(self):
		self.player.make_a_bet()
		self.initial_deal()
		self.log_hands()
		self.moves()
		self.dealer.compare(bkjk.people)
		self.another_round()

	def another_round(self):
		print('Another round?')
		answer = input()
		if answer == 'y':
			self.new_round()
			self.game()


def main(bkjk):
	bkjk.game()

if __name__ == '__main__':
	bkjk = Blackjack()
	main(bkjk)
