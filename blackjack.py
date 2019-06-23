from player import Player, Dealer
from shoe import Shoe


class Blackjack():
	def __init__(self, use_basic_strategy=False):
		self.use_basic_strategy = use_basic_strategy
		self.shoe = Shoe()
		self.player = Player(self.shoe)
		self.dealer = Dealer(self.shoe)
		self.people= [self.player, self.dealer]

	def initial_deal(self):
		for person in self.people:
			self.dealer.deal(shoe=self.shoe, person=person, num_of_cards=2)

	def new_round(self):
		for person in self.people:
			person.new_hand()

	def game(self):
		bkjk.initial_deal()
		# todo
		bkjk.new_round()


def main(bkjk):
	bkjk.game()

if __name__ == '__main__':
	bkjk = Blackjack()
	main(bkjk)
