from django.urls import path, include
from rest_framework import routers

from .views import RegistrationAPIView, NewsViewSet

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('', include(router.urls)),
]
