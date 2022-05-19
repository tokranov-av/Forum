from django.urls import path
from .views import RegistrationViewSet

urlpatterns = [
    path(
        'registration/', RegistrationViewSet.as_view(),
        name='registration'
    ),
]
