from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Article
from .serialisers import RegistrationSerializer, NewsSerializer
from django.contrib.auth import get_user_model
from .pagination import NewsPagination

User = get_user_model()


class RegistrationAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class NewsAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
