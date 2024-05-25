from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_otp_format(otp: str):
	if len(otp) != 6 or not otp.isdigit():
		raise ValidationError(
			_("Invalid OTP format")
		)
