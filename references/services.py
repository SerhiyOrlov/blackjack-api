def ask_number_of_players():
	number_of_players = input('| | How many players?\n| | ')
	try:
		number_of_players = int(number_of_players)
	except ValueError:
		print('| | VALUE ERROR. Only digits are accepteble')
		ask_number_of_players()
	if number_of_players < 1 or number_of_players > 6:
		print("ERROR. Maximum number of players is 6. Minimum is 2")
		ask_number_of_players()
	return number_of_players


def ask_names():
	for i in range(1, self.number_of_players):
		names[i] = input(f'| | Player {i}, what is your name?\n| | ')



