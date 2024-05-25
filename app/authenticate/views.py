from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.renderers import UserJSONRenderer
from .tasks import send_otp_email
from .serializers import (
	LoginSerializer,
	RegistrationSerializer,
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


