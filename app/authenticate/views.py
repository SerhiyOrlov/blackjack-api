from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.renderers import UserJSONRenderer

from .auth_services import send_otp
from .serializers import (
	LoginSerializer,
	RegistrationSerializer,
)


class RegistrationAPIView(APIView):
	"""
	API View for user registration
	"""
	permission_classes = (AllowAny,)
	serializer_class = RegistrationSerializer

	def post(self, request):
		"""
		Post requests handling for user registration.
		"""
		user = request.data.get('user', {})
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)

		if "email" not in serializer.validated_data.keys():
			return Response(data="Error. Email was not provided.", status=status.HTTP_400_BAD_REQUEST)

		if "confirmation_otp" not in serializer.validated_data.keys():
			return Response(data="Error. Error while generating OTP, try again later please",
							status=status.HTTP_503_SERVICE_UNAVAILABLE)

		# Sending a one-time password to the email provided by the user.
		email = serializer.validated_data.get("email")
		confirmation_otp = serializer.validated_data.get("confirmation_otp")
		send_otp_result = send_otp(email, confirmation_otp)
		if send_otp_result is None:
			return Response(data="Error. Imposible to send confirmation email try again later",
							status=status.HTTP_503_SERVICE_UNAVAILABLE)
		usr = serializer.save()
		return Response(data="OTP was successfuly sended", status=status.HTTP_200_OK)


class LoginAPIView(APIView):
	"""
	API View for user authentication
	"""
	permission_classes = (AllowAny,)
	renderer_classes = (UserJSONRenderer,)
	serializer_class = LoginSerializer

	def post(self, request):
		"""
		Post request handling for user authentication.
		"""
		user = request.data.get('user', {})

		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)

		return Response(serializer.data, status=status.HTTP_200_OK)
