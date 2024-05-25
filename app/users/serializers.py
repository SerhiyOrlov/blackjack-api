from rest_framework import serializers
from .models import User
from .validators import validate_otp_format


class UserSerializer(serializers.ModelSerializer):
	"""
	Serilizing and deserializing User objects
	"""
	password = serializers.CharField(
		max_length=128,
		min_length=8,
		write_only=True,
	)

	class Meta:
		model = User
		fields = (
			'email',
			'username',
			'password',
			'token',
			'balance',
		)
		read_only_fields = ('token',)

	def update(self, instance, validated_data):
		"""
		Perfoms a User update
		"""
		password = validated_data.pop('password', None)

		for key, value in validated_data.items():
			setattr(instance, key, value)  # Update every changed user attribute in user object
		if password is not None:
			instance.set_password(password)

		instance.save()

		return instance


class OTPSerializer(serializers.Serializer):
	"""
	Serializer for validationg OTP before checking it in database
	"""
	otp = serializers.CharField(validators=[validate_otp_format])