
values = [ 2, 3, 4, 5, 6, 7, 8, 9, 1, "J", "Q", "K", "A" ]
suits = [ "c", "d", "h", "s" ]

single_deck = [ str(value) + suit for value in values for suit in suits ]

def get_decks(number_of_decks):
	return single_deck * number_of_decks

def main():
	pass

if __name__ == '__main__':
	main()
