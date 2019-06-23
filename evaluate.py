from cards import high_values as high_value_cards

class Evaluate():

	high_values = high_value_cards

	def __init__(self):
		pass


	def evaluate_card_value(self, score, card):
		card = card[0]
		card_value = self.get_value(card)

		value_list = [score, card_value]

		if Evaluate.all_ints(value_list):
			return score + card_value
		elif Evaluate.all_lists(value_list):
			return [ x + 1 for x in score]
		else:
			return Evaluate.pack_list(value_list)


	def get_value(self, card):
		if card in Evaluate.high_values:
			value = Evaluate.high_values[card]
		else:
			value = int(card)
		return value


	@staticmethod
	def all_ints(value_list):
		return all([ type(x) is int for x in value_list])


	@staticmethod
	def all_lists(value_list):
		return all([ type(x) is list for x in value_list])


	@staticmethod
	def pack_list(value_list):
		value_list = sorted(value_list, key=lambda x: type(x) is list)
		cval = value_list[0]
		lst = value_list[1]
		lst = [ x + cval for x in lst]
		return Evaluate.check_values(lst)


	@staticmethod
	def check_values(lst):
		if max(lst) > 21:
			return min(lst)
		return lst


def main():
	pass

if __name__ == '__main__':
	main()
