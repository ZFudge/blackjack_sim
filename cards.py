
values = [ 2, 3, 4, 5, 6, 7, 8, 9, 1, "J", "Q", "K", "A" ]
suits = [ "c", "d", "h", "s" ]
single_deck = [ str(value) + suit for value in values for suit in suits ]


card_values = dict.fromkeys(['2', '3', '4', '5', '6'], 1)
card_values.update(dict.fromkeys(['7', '8', '9'], 0))
card_values.update(dict.fromkeys(['1', 'J', 'Q', 'K', 'A'], -1))


high_values = dict.fromkeys(['1', 'J', 'Q', 'K'], 10)
high_values['A'] = [1, 11]
