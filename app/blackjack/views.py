from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action  # ?

from users.models import User
from .models import Card, Hand, Game
from .serializers import CardSerializer, HandSerializer, GameSerializer

from django.shortcuts import get_object_or_404


class GameViewSet(viewsets.ViewSet):

	def create(self, request):
		user = request.user
		dealer_hand = Hand.objects.create(player=user)
		player_hand = Hand.objects.create(player=user)

		game = Game.objects.create(dealer_hand=dealer_hand)
		game.player_hands.add(player_hand)
		game.save()

		deck = self._create_deck()
		self._deal_initial_cards(deck, dealer_hand, player_hand)

		serializer = GameSerializer(game)
		return Response(serializer.data)

	def list(self, request):
		games = Game.objects.filter(active=True)
		serializer = GameSerializer(games, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		game = get_object_or_404(Game, pk=pk)
		serializer = GameSerializer(game)
		return Response(serializer.data)

	@action(detail=True, methods=['post'])
	def hit(self, request, pk=None):
		game = get_object_or_404(Game, pk=pk)
		user = request.user
		player_hand = game.player_hands.get(player=user)
		card = self._deal_card()
		player_hand.cards.add(card)
		player_hand.save()

		if player_hand.value() > 21:
			game.active = False  # ?
			game.save()
			return Response({"result": "Player busts! Dealer wins."}, status=status.HTTP_200_OK)

		serializer = GameSerializer(game)
		return Response(serializer.data)

	@action(detail=True, methods=['post'])
	def stand(self, request, pk=None):
		game = get_object_or_404(Game, pk=pk)
		self._dealer_play(game.dealer_hand)
		result = self._check_winner(game)
		game.active = False
		game.save()
		return Response({"result": result}, status=status.HTTP_200_OK)

	def _create_deck(self):
		deck = []
		for suit in Card.SUITS:
			for rank in Card.RANKS:
				deck.append(Card.objects.create(suit=suit[0], rank=rank[0]))
		return deck

	def _deal_initial_cards(self, deck, dealer_hand, player_hand):
		for _ in range(2):
			player_hand.cards.add(self._deal_card(deck))
			dealer_hand.cards.add(self._deal_card(deck))
		dealer_hand.save()
		player_hand.save()

	def _deal_card(self, deck):
		return deck.pop()

	def _dealer_play(self, dealer_hand):
		while dealer_hand.value() < 17:
			dealer_hand.cards.add(self._deal_card())
		dealer_hand.save()

	def _check_winner(self, game):
		dealer_value = game.dealer_hand.value()
		player_hand = game.player_hands.first()
		player_value = player_hand.value()

		if player_value > 21:
			return "Player busts! Dealer wins."
		elif dealer_value > 21 or player_value > dealer_value:
			return "Player wins!"
		elif player_value < dealer_value:
			return "Dealer wins!"
		else:
			return "Push! It's a tie."
