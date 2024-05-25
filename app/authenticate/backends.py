import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
	authentication_header_prefix = 'Token'

	def authenticate(self, request):
		request.user = None
		# What is auth header and auth header prefix and from where we can get it? (Not shure if spelling correct)
		auth_header = authentication.get_authorization_header(request).split()
		auth_header_prefix = self.authentication_header_prefix.lower()

		if not auth_header:
			return None

		if len(auth_header) == 1:
			# Incorrect token header, header contain only one element, must two
			return None

		elif len(auth_header) > 2:
			# Incorrect token header, some extra space symbols
			return None

		prefix = auth_header[0].decode('utf-8')
		token = auth_header[1].decode('utf-8')
		if prefix.lower() != auth_header_prefix:
			# Unexpected prefix -- failure
			return None

		return self._authenticate_credentials(request, token)

	def _authenticate_credentials(self, request, token):
		"""
		Trying to authenitcate with provided credentials.
		If succsess - return User object and token, otherwise generate an exception
		"""

		try:

			payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
		except Exception:
			msg = "Authenticate error. Unable to decode token"
			raise exceptions.AuthenticationFailed(msg)\

		try:
			user = User.objects.get(pk=payload['id'])
		except User.DoesNotExist:
			msg = 'A user corresponding to this token was not found.'
			raise exceptions.AuthenticationFailed(msg)

		if not user.is_active:
			msg = 'This user is not active'
			raise exceptions.AuthenticationFailed(msg)

		return user, token
