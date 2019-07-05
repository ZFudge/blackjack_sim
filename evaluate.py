from cards import high_values as high_value_cards

class Evaluate():
	high_values = high_value_cards

	def evaluate_card_value(self, score, card):
		card_value = self.get_value(card)
		value_list = [score, card_value]

		if Evaluate.all_ints(value_list):
			return score + card_value
		elif Evaluate.all_lists(value_list):
			return Evaluate.prune_gt21_list([ x + 1 for x in score])
		elif Evaluate.mix_int_and_list(value_list):
			return Evaluate.pack_list(value_list)
		else:
			raise ValueError(f'Score types can only include int and list. Current types include {[type(x) for x in value_list]}')


	def get_value(self, card):
		if card in Evaluate.high_values:
			value = Evaluate.high_values[card]
		else:
			value = int(card)
		return value


	@staticmethod
	def prune_gt21_list(score_list):
		if max(score_list) > 21:
			return min(score_list)
		return score_list

	@staticmethod
	def all_ints(value_list):
		return all([ type(x) is int for x in value_list])

	@staticmethod
	def all_lists(value_list):
		return all([ type(x) is list for x in value_list])

	@staticmethod
	def mix_int_and_list(value_list):
		types = [ type(x) for x in value_list]
		return int in types and list in types

	@staticmethod
	def pack_list(value_list):
		value_list = sorted(value_list, key=lambda x: type(x) is list)
		cval = value_list[0]
		lst = value_list[1]
		lst = [ x + cval for x in lst]
		return Evaluate.prune_gt21_list(lst)


def main():
	pass

if __name__ == '__main__':
	main()
