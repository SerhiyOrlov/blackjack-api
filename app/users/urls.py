from django.urls import path

from .views import UserRetriveUpdateView, UserBalanceView

urlpatterns = [
	path('', UserRetriveUpdateView.as_view()),
	path('balance/', UserBalanceView.as_view())
]