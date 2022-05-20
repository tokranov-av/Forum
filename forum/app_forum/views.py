from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import filters, mixins, permissions, status
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Article, UserRatingsOfArticles
from .serialisers import (
    RegistrationSerializer, NewsSerializer, NewsDetailSerializer
)
from django.contrib.auth import get_user_model
from .pagination import NewsPagination
from rest_framework.decorators import action
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response

User = get_user_model()


class RegistrationAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class NewsViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Article.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('rating', 'date_create',)
    ordering = ('-rating',)
    lookup_field = 'slug'
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = NewsDetailSerializer(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def vote(self, request, *args, **kwargs):
        current_user = request.user
        current_news = self.get_object()

        if isinstance(current_user, AnonymousUser):
            data = {'message': 'Пожалуйста, авторизуйтесь.'}
            return Response(data)

        user_rating = UserRatingsOfArticles.objects.filter(
            user=current_user, article=current_news)

        return Response({'message': 'Вы поставили Like пользователю.'})


# class NewsAPIView(ListAPIView):
#     queryset = Article.objects.all()
#     serializer_class = NewsSerializer
#     pagination_class = NewsPagination
#     filter_backends = (filters.OrderingFilter,)
#     ordering_fields = ('rating', 'date_create',)
#     ordering = ('-rating',)
#
#
# class NewsDetailAPIView(ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = NewsDetailSerializer
#     lookup_field = 'slug'
#
#     @action(methods=['get'], detail=True)
#     def vote(self, request, *args, **kwargs):
#         current_user = request.user
#         current_news = self.get_object()
#
#         if isinstance(current_user, AnonymousUser):
#             data = {'message': 'Пожалуйста, авторизуйтесь.'}
#             return Response(data)
#
#         user_rating = UserRatingsOfArticles.objects.filter(
#             user=current_user, article=current_news)
#
#         return Response({'message': 'Вы поставили Like пользователю.'})
