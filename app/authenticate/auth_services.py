from .tasks import send_otp_email


def send_otp(email, confirmation_otp):
	try:
		send_otp_email.delay(email, confirmation_otp)
		return True
	except Exception as e:
		print(e)


