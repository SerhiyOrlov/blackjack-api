from consts import SUITS, VALUES, DEBUG
from services import (
	ask_number_of_players,
					)


class BlackJack:
	def __init__(self, players: list[dict]):
		self.players = players

	def run(self):
		print(self.players)


def set_players(number_of_players: int) -> list[dict]:
	players = list()
	if not number_of_players:
		raise "Error. number_of_players can't be None"

	for i in range(1, number_of_players):
		print(f"| | --- Player {i} ---| |")
		name = input('| | What is your name?| |\n')
		bet = input(f"| |Welcome, {name}. What is your bet? | |\n")
		players.append({"name": name, "bet": bet})
	return players


def main():
	if DEBUG:
		print("You are in debug mode")
		players = [{"name": "Ihor", "bet": 50}, {"name": "Alex", "bet":70}]
	else:
		number_of_players = ask_number_of_players()
		print(number_of_players)
		players = set_players(number_of_players)

	blackjack_operator = BlackJack(players=players)
	blackjack_operator.run()


if __name__ == "__main__":
	main()
