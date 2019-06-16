from cards import counts as card_counts

class Count():

	counts = card_counts

	def __init__(self):
		self.count = 0
		self.true_count = 0


	def count_card(self, card):
		card = card[0]
		self.count += self.hi_lo(card)


	def deck_size_to_true_count(self, deck_size):
		self.true_count = self.count / deck_size


	@classmethod
	def hi_lo(cls, card):
		cards = cls.counts['cards']
		if card in cards['lo']:
			count = 'lo'
		elif card in cards['md']:
			count = 'md'
		elif card in cards['hi']:
			count = 'hi'
		return cls.counts['values'][count]


def main():
	pass

if __name__ == '__main__':
	main()
