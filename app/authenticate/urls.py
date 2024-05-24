from django.urls import path

from .views import RegistrationAPIView, UserRetriveUpdateView, LoginAPIView, UserBalanceView

urlpatterns = [
	path('registration/', RegistrationAPIView.as_view()),
	path('user/', UserRetriveUpdateView.as_view()),
	path('users/login/', LoginAPIView.as_view()),
	path('user/balance', UserBalanceView.as_view())
]