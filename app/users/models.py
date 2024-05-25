"""Mixin - A Addtional class to expand base class functionality"""

import jwt

from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from django.conf import settings  # Importing Django settings
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	PermissionsMixin  # PermissionMixin allows to add pemissions at the User model
)

from django.db import models


class UserManager(BaseUserManager):
	"""
	UserManager is a required class for User model.
	Needed for managing User objects.
	"""

	def create_user(self, username, email, password=None):
		"""Creating a usual user without additonal permissions."""
		if username is None:
			raise TypeError('Users must have a username.')

		if email is None:
			raise TypeError('Users must have an email address.')

		user = self.model(username=username, email=self.normalize_email(email))
		user.set_password(password)  # A default Django method to set normalized and hashed password to the user
		user.save()

		return user

	def create_superuser(self, username, email, password):
		"""Create superuser who has permission to the admin panel"""
		if password is None:
			raise TypeError('Superusers must have a password.')

		user = self.create_user(username, email, password)
		user.is_superuser = True  # User has all permissions of applications
		user.is_staff = True  # User has permission to the admin panel, and superuser can set some restrictions
		user.save()

		return user


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(db_index=True, max_length=255, unique=True)
	email = models.EmailField(db_index=True, unique=True)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	balance = models.IntegerField(default=0)
	confirmation_otp = models.IntegerField(verbose_name=_("OTP"), null=True, blank=True)

	USERNAME_FIELD = 'email'  # Email instead username in user authentications
	REQUIRED_FIELDS = ('username',)

	objects = UserManager()

	def __str__(self):
		"""Email as preview of the model in admin panel"""
		return self.email

	@property
	def token(self):
		"""Function with property decorator allows to add an edditional atribute to the class"""
		return self._generate_jwt_token()

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def get_balance(self):
		return self.balance

	def append_balance(self, value):
		self.balance += value
		return self.balance

	def _generate_jwt_token(self):
		"""
		Generating jwt token.
		Payload : id: User.pk, exp: Datetime obj(Now + 1 day)
		"""
		dt = datetime.now() + timedelta(days=1)

		token = jwt.encode({
			'id': self.pk,
			'exp': int(dt.strftime('%s'))
		}, settings.SECRET_KEY, algorithm='HS256')

		return token
