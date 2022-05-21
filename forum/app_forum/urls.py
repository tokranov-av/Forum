from django.urls import path, include
from rest_framework import routers

from .views import RegistrationAPIView, NewsViewSet, AddNewsAPIView

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('news/add/', AddNewsAPIView.as_view(), name='add_news'),
    path('', include(router.urls)),
]
