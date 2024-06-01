from rest_framework import serializers
from users.models import User
from .models import Card, Hand, Game


class CardSerializer(serializers.ModelSerializer):
	"""Serializer for Card model."""
	class Meta:
		model = Card
		fields = ['id', 'suit', 'rank']


class HandSerializer(serializers.ModelSerializer):
	"""Serializer for Hand model."""
	cards = CardSerializer(many=True)

	class Meta:
		model = Hand
		fields = ['id', 'player', 'cards', 'value']


class GameSerializer(serializers.ModelSerializer):
	"""Serializer for the Game model."""
	dealer_hand = HandSerializer()
	player_hands = HandSerializer(many=True)

	class Meta:
		model = Game
		fields = ['id', 'dealer_hand', 'player_hands', 'active']
