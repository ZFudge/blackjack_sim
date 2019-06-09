import random

class Deck():
	values = [ 2, 3, 4, 5, 6, 7, 8, 9, 1, "J", "Q", "K", "A" ]
	suits = [ "c", "d", "h", "s" ]

	def __init__(self):
		Deck.single_deck = [ str(value) + suit for value in Deck.values for suit in Deck.suits ]
		self.shoe = []

	def draw():
		return self.shoe.pop()

	def get_decks(self, number_of_decks, penetration_percentage):
		shuffled_decks = Deck.shuffle(Deck.single_deck * number_of_decks)
		penetrated_decks = Deck.penetrate(shuffled_decks, penetration_percentage)
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
