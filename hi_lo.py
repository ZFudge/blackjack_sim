from cards import card_count_values


class Hi_Lo():
	count = 0
	true_count = 0

	@classmethod
	def count_card(cls, card_shoesize):
		card, shoesize = card_shoesize
		card = card[0]
		print(f'count: {cls.count}, true_count: {cls.true_count}, value:{card_count_values[card]}', end='')
		cls.count += card_count_values[card]
		cls.set_true_count(shoesize)
		print(f'    card: {card}, shoesize: {shoesize}, count: {cls.count}, true_count: {cls.true_count}')#, end='')


	@classmethod
	def set_true_count(cls, deckcount):
		if deckcount > 1:
			cls.true_count = round(cls.count / deckcount)
		else:
			cls.true_count = cls.count


	@classmethod
	def reset_count(cls):
		cls.count = 0
		cls.true_count = 0


def main():
	pass

if __name__ == '__main__':
	main()
