from cards import single_deck as single_deck_list

import random

class Shoe():
	single_deck = single_deck_list

	def __init__(self, hl=None, number_of_decks=8, penetration_percentage=65):
		self.hl = hl
		self.shoe = []
		self._number_of_decks = number_of_decks
		self._penetration_percentage = penetration_percentage
		self.new_shoe()
		self._full_shoe = self.number_of_cards


	def draw(self):
		card = self.shoe.pop()
		if len(self.shoe) == 0:
			self.new_shoe()
		return card

	def full(self, count):
		return self.number_of_cards == self.full_shoe or self.full_shoe - self.number_of_cards < abs(count)

	def new_shoe(self):
		print('\t\t\tnew shoe')
		shuffled_decks = Shoe.shuffle(Shoe.single_deck * self.number_of_decks)
		penetrated_decks = Shoe.penetrate(shuffled_decks, self.penetration_percentage)
		self.shoe = penetrated_decks
		if self.hl is not None:
			self.hl.reset_count()

	@property
	def size(self):
		return round(2 * (len(self.shoe) / (self.penetration_percentage / 100 * 52))) / 2

	@property
	def number_of_decks(self):
		return self._number_of_decks

	@number_of_decks.setter
	def number_of_decks(self, value):
		if type(value) is int:
			if value >= 1 and value <= 8:
				self._number_of_decks = value
				self.new_shoe()
			else:
				raise ValueError(f'Deck number must be between 1 and 8. Received {value}')
		else:
			raise ValueError(f'Deck number type must be int. Received {type(value)}')

	@property
	def number_of_cards(self):
		return len(self.shoe)

	@property
	def full_shoe(self):
		return self._full_shoe

	@property
	def penetration_percentage(self):
		return self._penetration_percentage

	@penetration_percentage.setter
	def penetration_percentage(self, value):
		if type(value) is int:
			if value >= 60 and value <= 100:
				self._penetration_percentage = value
				self.new_shoe()
			else:
				raise ValueError(f'Penetration percentage must be between 60 and 100. Received {value}')
		else:
			raise ValueError(f'Penetration percentage type must be int. Received {type(value)}')

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
