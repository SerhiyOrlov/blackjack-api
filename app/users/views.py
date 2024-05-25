from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from .serializers import (
	UserSerializer,
	OTPSerializer,
)

from .models import User

from .renderers import UserJSONRenderer


class UserBalanceView(generics.RetrieveUpdateAPIView):
	"""
	An endpoint for getting or updating the balance of a user.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = UserSerializer

	def retrieve(self, request, *args, **kwargs):
		serializer = self.serializer_class(request.user)
		return Response({"balance": serializer.data.get('balance')}, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		serializer_data = request.data.get('user', {})
		params = request.query_params
		if params:
			new_balance = params.get('balance', None)
			if new_balance is not None:
				serializer_data['balance'] = new_balance

		serializer = self.serializer_class(
			request.user,
			data=serializer_data,
			partial=True
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetriveUpdateView(generics.RetrieveUpdateAPIView):
	"""
	An endpoint for getting a specific user and updating their information.
	"""
	permission_classes = (IsAuthenticated,)
	renderer_classes = (UserJSONRenderer,)
	serializer_class = UserSerializer

	def retrieve(self, request, *args, **kwargs):
		serializer = self.serializer_class(request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			raise PermissionDenied()
		serializer_data = request.data.get('user', {})
		serializer = self.serializer_class(
			request.user,
			data=serializer_data,
			partial=True
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_200_OK)


class UserConfirmOTPView(generics.GenericAPIView):
	"""
	An endpoint for the one-time password confirmation
	"""
	serializer_class = OTPSerializer

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		otp = serializer.data['otp']
		if not settings.TOTP_GENERATOR.verify(otp):
			return Response(data="OTP expired", status=status.HTTP_401_UNAUTHORIZED)

		user = get_object_or_404(User, confirmation_otp=otp)
		user.confirmation_otp = None
		user.is_active = True
		user.save()
		return Response({
			"user": UserSerializer(user, context=self.get_serializer_context()).data,
			"message": "User confirmed successfully",
		})
