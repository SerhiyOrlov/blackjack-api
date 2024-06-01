from users.models import User
from django.db import models


class Card(models.Model):
	SUITS = (
		('Hearts', 'Hearts'),
		('Diamonds', 'Diamonds'),
		('Clubs', 'Clubs'),
		('Spades', 'Spades'),
	)
	RANKS = (
		('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
		('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
		('J', 'Jack'), ('Q', 'Queen'), ('K', 'King'), ('A', 'Ace'),
	)

	suit = models.CharField(max_length=8, choices=SUITS)
	rank = models.CharField(max_length=5, choices=RANKS)

	def value(self):
		if self.rank in ['J', 'Q', 'K']:
			return 10
		elif self.rank == 'A':
			return 1
		else:
			try:
				return int(self.rank)
			except ValueError:
				raise "Card model. ert6bb7n "

	def __str__(self):
		return f"{self.rank} of {self.suit}"


class Hand(models.Model):
	player = models.ForeignKey(User, on_delete=models.CASCADE)
	cards = models.ManyToManyField("Card")

	def value(self):
		total = 0
		aces = 0
		for card in self.cards.all():
			total += card.value()
			if card.rank == 'A':
				aces += 1
		while total + 10 <= 21 and aces > 0:
			total += 10
			aces -= 1
		return total

	def __str__(self):
		return ', '.join([str(card) for card in self.cards.all()])


class Game(models.Model):
	dealer_hand = models.OneToOneField("Hand", related_name='dealer_hand', on_delete=models.CASCADE)
	player_hands = models.ManyToManyField("Hand", related_name='player_hands')
	active = models.BooleanField(default=True)

	def __str__(self):
		return f"Game {self.id}"
