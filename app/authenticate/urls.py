from django.urls import path

from .views import RegistrationAPIView, LoginAPIView

urlpatterns = [
	path('registration/', RegistrationAPIView.as_view()),
	path('login/', LoginAPIView.as_view()),
]