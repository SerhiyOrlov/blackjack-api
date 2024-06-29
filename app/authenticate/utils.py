import jwt

from django.conf import settings
from datetime import datetime, timedelta


class AuthManager:
	@staticmethod
	def generate_token(user_id):
		# Валидация входных данных
		if not isinstance(user_id, int):
			raise ValueError("User ID must be an integer")
		# Логирование
		print(f"Generating token for user_id: {user_id}")
		# Вызов приватного статического метода для генерации токена
		return AuthManager._generate_jwt_token(user_id)

	@staticmethod
	def refresh_token(old_token):
		# Валидация входных данных
		if not isinstance(old_token, str) or not old_token.startswith("jwt_token_for_user_"):
			raise ValueError("Invalid token format")
		# Логика обновления токена, возможно, с вызовом _generate_jwt_token
		user_id = AuthManager._extract_user_id_from_token(old_token)
		return AuthManager._generate_jwt_token(user_id)

	@staticmethod
	def _generate_jwt_token(user_id):
		"""
		Generating jwt token.
		Payload : id: User.pk, exp: Datetime obj(Now + 1 day)
		"""
		dt = datetime.now() + timedelta(days=1)

		token = jwt.encode({
			'id': user_id,
			'exp': int(dt.strftime('%s'))
		}, settings.SECRET_KEY, algorithm='HS256')

		return token

	@staticmethod
	def _extract_user_id_from_token(token):
		# Вспомогательный метод для извлечения user_id из токена
		try:
			user_id = int(token.split('_')[-1])
		except (IndexError, ValueError):
			raise ValueError("Invalid token format")
		return user_id

	@staticmethod
	def decode_jwt_token(token):
		try:
			payload = jwt.decode(token, settings.JWT_AUTH['JWT_SECRET_KEY'],
			                     algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']])
			return payload
		except jwt.ExpiredSignatureError:
			return None
		except jwt.InvalidTokenError:
			return None




