from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .renderers import UserJSONRenderer
from .tasks import send_otp_email
from .serializers import (
	LoginSerializer,
	RegistrationSerializer,
	UserSerializer,
	OTPSerializer,
)


class RegistrationAPIView(APIView):
	permission_classes = (AllowAny,)
	serializer_class = RegistrationSerializer

	def post(self, request):
		user = request.data.get('user', {})
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		# Send OTP
		if "email" not in serializer.data.keys() or "confirmation_otp" not in serializer.data.keys():
			print(serializer.data.keys())
			return Response(data="Error. Imposible to send confirmation email try again later",
			                status=status.HTTP_503_SERVICE_UNAVAILABLE)
		print(serializer.data.get("email"), serializer.data.get('confirmation_otp'))
		try:
			send_otp_email.delay(serializer.data.get("email"), serializer.data.get('confirmation_otp'))
		except Exception as e:
			return Response("Error sending confirmation email try again later",
			                status=status.HTTP_503_SERVICE_UNAVAILABLE)
		# serializer.save()
		return Response(data="OTP sent", status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
	permission_classes = (AllowAny,)
	renderer_classes = (UserJSONRenderer,)
	serializer_class = LoginSerializer

	def post(self, request):
		user = request.data.get('user', {})

		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)

		return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetriveUpdateView(generics.RetrieveUpdateAPIView):
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


class UserBalanceView(generics.RetrieveUpdateAPIView):
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


class UserConfirmOTPView(generics.GenericAPIView):
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
