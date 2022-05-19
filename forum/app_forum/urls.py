from django.urls import path
from .views import RegistrationAPIView, NewsAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('news/', NewsAPIView.as_view(), name='news'),
]
