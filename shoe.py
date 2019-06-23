from cards import single_deck as single_deck_list
import random

class Shoe():

	single_deck = single_deck_list

	def __init__(self, number_of_decks=8, penetration_percentage=65):
		self.shoe = []
		self._number_of_decks = number_of_decks
		self._penetration_percentage = penetration_percentage
		self.new_shoe()


	@property
	def deck_count(self):
		return round(len(self.shoe) / (self.penetration_percentage / 100 * 52))


	@property
	def number_of_decks(self):
		return self._number_of_decks


	@number_of_decks.setter
	def number_of_decks(self, value):
		self._number_of_decks = value


	@property
	def penetration_percentage(self):
		return self._penetration_percentage


	@penetration_percentage.setter
	def penetration_percentage(self, value):
		self._penetration_percentage = value


	def draw(self):
		card = self.shoe.pop()
		if len(self.shoe) == 0:
			self.new_shoe()
		return card


	def new_shoe(self):
		shuffled_decks = Shoe.shuffle(Shoe.single_deck * self.number_of_decks)
		penetrated_decks = Shoe.penetrate(shuffled_decks, self.penetration_percentage)
		self.shoe += penetrated_decks


	@staticmethod
	def shuffle(deck):
		deck_length = len(deck)
		for x in range(1000):
			index = random.randint(1, deck_length - 1)
			mid_card = deck.pop(index)
			end_card = deck.pop()
			inverted_index = abs(index - deck_length)
			deck = [mid_card] + deck[:inverted_index] + [end_card] + deck[inverted_index:]
		return deck


	@staticmethod
	def penetrate(deck, percentage):
		cutoff_index = int(len(deck) * (percentage / 100.0))
		return deck[:cutoff_index]


def main():
	pass

if __name__ == '__main__':
	main()
