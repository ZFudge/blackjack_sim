from cards import high_values as high_value_cards

class Evaluate():

	high_values = high_value_cards

	def __init__(self):
		pass


	def evaluate(self, c1, c2):
		v1 = self.get_value(c1)
		v2 = self.get_value(c2)
		val_list = [v1, v2]
		if self.check_ints(val_list):
			return v1 + v2
		else:
			return self.pack_list(val_list)


	def get_value(self, card):
		card = card[0]
		if card in Evaluate.high_values:
			value = Evaluate.high_values[card]
		else:
			value = int(card)
		return value


	def pack_list(self, lst):
		if type(lst[0]) is list:
			target_list = lst[0]
			add_val = lst[1]
		else:
			target_list = lst[1]
			add_val = lst[0]
		return [ x + add_val for x in target_list]


	def check_ints(self, lst):
		is_int_list = self.get_types(lst)
		return all(is_int_list)


	def get_types(self, lst):
		return [ type(x) is int for x in lst]


def main():
	pass

if __name__ == '__main__':
	main()
