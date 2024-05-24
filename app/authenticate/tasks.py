from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task()
def send_otp_email(to_email, otp):
	subject = "Confirmation OTP"
	message = f"Hello! \n" \
	          f"Congradilations! \n" \
	          f"You are just steps away from the game\n" \
	          f"Please confirm your email using this one time password\n" \
	          f"<b>{otp}</b>" \
	          f"It's expiration time: {settings.OTP_EXPIRATION_IN_MINUTES} minutes."

	from_email = settings.EMAIL_HOST_USER
	recipient_list = [to_email]
	send_mail(subject, message, from_email, recipient_list)
#  send_otp_email.delay("s.orlov11012@gmail.com", 554433)
