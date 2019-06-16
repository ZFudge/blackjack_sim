class Count():
	counts =  {
		'cards': {
			'lo': ['2', '3', '4', '5', '6'],
			'md': ['7', '8', '9'],
			'hi': ['1', 'J', 'Q', 'K', 'A']
		},
		'values': {
			"lo": -1,
			"md": 0,
			"hi": 1
		}
	}

	def __init__(self):
		self.count = 0
		self.true_count = 0

	def count_card(self, card):
		card = card[0]
		self.count += self.increment_count(card)

	def increment_count(self, card):
		if card in Count.counts['cards']['lo']:
			count = 'lo'
		elif card in Count.counts['cards']['md']:
			count = 'md'
		elif card in Count.counts['cards']['hi']:
			count = 'hi'
		return Count.counts['values'][count]

	def calculate_true_count(self):
		pass