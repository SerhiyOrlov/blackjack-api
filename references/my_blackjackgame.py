from consts import SUITS, VALUES, DEBUG, INITIAL_BALANCE
from services import (
	ask_number_of_players,
					)


class BlackJack:
	def __init__(self, players: list[dict]):
		self.players = players

	@staticmethod
	def create_deck():
		deck = []
		for suit in range(4):
			for value in range(13):
				deck.append((suit, value))
		return deck

	def run(self):
		print(self.players)


def set_players(number_of_players: int) -> list[dict]:
	players = list()
	if not number_of_players:
		raise "Error. number_of_players can't be None"
	for i in range(number_of_players):
		player_number_ = i + 1
		print(f"| | --- Player {player_number_} --- | |")
		name = input('| | What is your name?| |\n')
		bet = int(input(f"| |Welcome, {name}. What is your bet? | |\n"))
		balance = INITIAL_BALANCE
		while bet > balance:
			print("Your don't have enought money on balance for this bet")
			bet = int(input(f"| |{name}, so what is your bet? | |\n"))
		players.append({"name": name, "bet": bet, "balance": balance})
	return players


def main():
	if DEBUG:
		print("You are in debug mode")
		players = [
					{"name": "Ihor", "bet": 50, 'balance': INITIAL_BALANCE},
					{"name": "Alex", "bet": 70, "balance": INITIAL_BALANCE},
																			]
	else:
		number_of_players = ask_number_of_players()
		players = set_players(number_of_players)

	blackjack_operator = BlackJack(players=players)
	blackjack_operator.run()


if __name__ == "__main__":
	main()
