from cards import card_value

class Hi_Lo():

	card_value = card_value

	def __init__(self):
		self._count = 0
		self._true_count = 0


	# def count_cards(self, card):
	# 	card = card[0]
	# 	self.count += self.count(card)


	# def deck_size_to_true_count(self, deck_size):
	# 	self.true_count = self.count / deck_size


	# @classmethod
	# def count(cls, card):
	# 	cards = cls.counts['cards']
	# 	if card in cards['lo']:
	# 		count = 'lo'
	# 	elif card in cards['md']:
	# 		count = 'md'
	# 	elif card in cards['hi']:
	# 		count = 'hi'
	# 	return cls.counts['values'][count]


	@property
	def count(self):
		return self._count

	@count.setter
	def count(self, card):
		card = card[0]
		self._count += card_value[card]

	@property
	def true_count(self):
		return self._true_count

	@true_count.setter
	def true_count(self, deck_count):
		self._true_count = self._count / deck_count

def main():
	pass

if __name__ == '__main__':
	main()
