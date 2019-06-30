from player import Player, Dealer

class Blackjack():
	def __init__(self, use_basic_strategy=False, stand_on_soft_17=True):
		self.dealer = Dealer(stand_on_soft_17=stand_on_soft_17)
		self.player = Player(use_basic_strategy=use_basic_strategy)
		self.people = [self.dealer, self.player]


	def game(self):
		self.player.make_a_bet()
		self.initial_deal()
		self.log_hands()
		self.make_moves()
		self.dealer.compare_people(self.people)
		self.next_round_check()


	def initial_deal(self):
		num_cards = 1
		for person in self.people:
			self.dealer.deal(person=person, num_of_cards=num_cards)
			num_cards += 1


	def log_hands(self):
		for person in self.people:
			person.log_hand()


	def make_moves(self):
		self.player.move()
		if not self.player.busted:
			self.dealer.move()


	def next_round_check(self):
		if self.player.use_basic_strategy or self.manual_round_check():
			self.new_round()
			self.game()


	def manual_round_check(self):
		answer = self.get_answer()
		if answer.startswith('y'):
			return True
		else:
			print('Bye.')


	@staticmethod
	def get_answer():
		answer = ''
		while answer not in ['y', 'ys', 'yes', 'n', 'no']:
			print('Play another round?: ', end='')
			answer = input().lower().strip()
		return answer


	def new_round(self):
		for person in self.people:
			person.new_hand()


def main():
	bkjk = Blackjack()
	bkjk.game()

if __name__ == '__main__':
	main()
