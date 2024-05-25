from django.urls import path

from .views import UserRetriveUpdateView, UserBalanceView, UserConfirmOTPView

urlpatterns = [
	path('', UserRetriveUpdateView.as_view()),
	path('balance/', UserBalanceView.as_view()),
	path('confirm_otp/', UserConfirmOTPView.as_view())
]
