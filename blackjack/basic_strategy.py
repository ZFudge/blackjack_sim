class Basic_Strategy():
	def __init__(self, stand_on_soft_17=True):
		self.strategy_map = Basic_Strategy.basic_strategy_map['s17' if stand_on_soft_17 else 'h17']

	s = 's' 	# stand
	h = 'h' 	# hit
	ds = 'ds' 	# double else standit
	dh = 'dh' 	# double else hit
	p = 'p' 	# split
	ns = 'ns' 	# no split
	ph = 'ph' 	# split if double allowed after else hit
	rh = 'rh'	# surrender if allowed else hit

	always_stands = [s] * 10
	always_hits = [h] * 10
	always_splits = [p] * 10
	never_splits = [ns] * 10

	basic_strategy_map = {
		's17': {
			'hard': {
				4: always_hits,
				5: always_hits,
				6: always_hits,
				7: always_hits,
				8: always_hits,
				9:  [ h,dh,dh,dh,dh, h, h, h, h, h ],
				10: [dh,dh,dh,dh,dh,dh,dh,dh, h, h ],
				11: [dh,dh,dh,dh,dh,dh,dh,dh,dh, h ],
				12: [ h, h, s, s, s, h, h, h, h, h ],
				13: [ s, s, s, s, s, h, h, h, h, h ],
				14: [ s, s, s, s, s, h, h, h, h, h ],
				15: [ s, s, s, s, s, h, h, h,rh, h ],
				16: [ s, s, s, s, s, h, h,rh,rh,rh ],
				17: always_stands,
				18: always_stands,
				19: always_stands,
				20: always_stands,
				21: always_stands
			},
			'soft': {
				13: [ h, h, h,dh,dh, h, h, h, h, h ],
				14: [ h, h, h,dh,dh, h, h, h, h, h ],
				15: [ h, h,dh,dh,dh, h, h, h, h, h ],
				16: [ h, h,dh,dh,dh, h, h, h, h, h ],
				17: [ h,dh,dh,dh,dh, h, h, h, h, h ],
				18: [ s,ds,ds,ds,ds, s, s, h, h, h ],
				19: always_stands,
				20: always_stands,
				21: always_stands
			},
			'split': {
				2: [ph,ph, p, p, p, p, h, h, h, h],
				3: [ph,ph, p, p, p, p, h, h, h, h],
				4: [ h, h, h,ph,ph, h, h, h, h, h],
				5: never_splits,
				6: [ph, p, p, p, p, h, h, h, h, h],
				7: [ p, p, p, p, p, p, h, h, h, h],
				8: always_splits,
				9: [ p, p, p, p, p, s, p, p, s, s],
				10: never_splits,
				'A': always_splits
			}
		},
		'h17': {}
	}


def main():
	pass

if __name__ == '__main__':
	main()
