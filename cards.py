
values = [ 2, 3, 4, 5, 6, 7, 8, 9, 1, "J", "Q", "K", "A" ]
suits = [ "c", "d", "h", "s" ]
single_deck = [ str(value) + suit for value in values for suit in suits ]


counts =  {
	'cards': {
		'lo': ['2', '3', '4', '5', '6'],
		'md': ['7', '8', '9'],
		'hi': ['1', 'J', 'Q', 'K', 'A']
	},
	'values': {
		'lo': -1,
		'md': 0,
		'hi': 1
	}
}


high_values = dict.fromkeys(['1', 'J', 'Q', 'K'], 10)
high_values['A'] = [1, 11]

