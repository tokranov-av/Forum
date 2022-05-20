from django.urls import path, include
from rest_framework import routers

from .views import RegistrationAPIView, NewsViewSet

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)
print(router.urls)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('', include(router.urls)),
    # path('news/', NewsViewSet.as_view({'get': 'list'}), name='news'),
    # path('news/<slug:slug>/', NewsViewSet.as_view({'get': 'retrieve'}), name='news_detail'),
]
