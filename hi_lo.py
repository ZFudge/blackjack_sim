from cards import card_values


class Hi_Lo():
	card_values = card_values

	def __init__(self):
		self._count = 0
		self._true_count = 0

	@property
	def count(self):
		return self._count

	@count.setter
	def count(self, card_shoesize):
		card, shoesize = card_shoesize
		card = card[0]
		self._count += card_values[card]
		self.true_count = shoesize

	@property
	def true_count(self):
		return self._true_count

	@true_count.setter
	def true_count(self, deck_count):
		if deck_count > 0:
			self._true_count = round(self._count / deck_count)
		else:
			self._true_count = self._count

	def reset_count(self):
		self._count = 0

def main():
	pass

if __name__ == '__main__':
	main()
