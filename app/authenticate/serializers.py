from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
	email = serializers.CharField()
	password = serializers.CharField(
		max_length=128,
		min_length=8,
		write_only=True
	)
	token = serializers.CharField(min_length=255, read_only=True)
	confirmation_otp = serializers.SerializerMethodField('get_confirmation_otp')

	def get_confirmation_otp(self, obj):
		return settings.TOTP_GENERATOR.now()

	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'token', 'confirmation_otp']

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)

	def validate(self, data):
		# include the additional field in the validated data
		data['confirmation_otp'] = self.get_confirmation_otp(self.instance)
		return super().validate(data)


class LoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=255)
	username = serializers.CharField(max_length=255, read_only=True)
	password = serializers.CharField(max_length=128, write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	def validate(self, data):
		email = data.get('email', None)
		password = data.get('password', None)

		if email is None:
			raise serializers.ValidationError(
				'A email address is required to log in'
			)

		if password is None:
			raise serializers.ValidationError(
				'A password is required to log in'
			)

		user = authenticate(username=email, password=password)  # Return either User model or none

		if user is None:
			raise serializers.ValidationError(
				'A user with this email and password was not found.'
			)

		if not user.is_active:
			raise serializers.ValidationError(
				'This user has benn deactivated.'
			)
		return {
			'email': user.email,
			'username': user.username,
			'token': user.token
		}
