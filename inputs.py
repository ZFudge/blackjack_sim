import re

def ask_for_another_round():
	choices = ['', 'y', 'ys', 'yes', 'n', 'no']
	answer = '"'
	while answer not in choices:
		print('Play another round?: ', end='')
		answer = input().lower().strip()
	return answer


def check_same_bet():
	choices = ['', 'y', 'ys', 'yes', 'n', 'no']
	new_bet = '"'
	while new_bet not in choices:
		print('Same bet?: ', end='')
		new_bet = input().lower().strip()
	return new_bet in choices[:-2]


def input_bet(bankroll):
	bet = 0
	while bet < 1 or bet > bankroll:
		print('Make a bet: $', end='')
		bet = re.sub('[^0-9]','', input())
		if len(bet) == 0:
			bet = 0
		else:
			bet = int(bet)
			if bet > bankroll:
				print('Bet cannot exceed bankroll.')
	return bet


def manual_move():
	choices = ['', 'h', 's', 'd', 'p']
	move_choice = '"'
	while move_choice not in choices: # , 'p'
		print('Make a move ([h]it, [s]tand, [d]ouble): ', end='') # , s[p]lit
		move_choice = input().lower().strip()
	return move_choice[:2]

