from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveAPIView, get_object_or_404
from rest_framework import filters, mixins, permissions, status
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet

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


class NewsViewSet(ViewSet):
    queryset = Article.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('rating', 'date_create',)
    ordering = ('-rating',)
    lookup_field = 'slug'

    def list(self, request, slug=None):
        queryset = Article.objects.all()
        serializer = NewsSerializer(queryset, many=True)
        serializer.context['request'] = request
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        queryset = Article.objects.all()
        instance = get_object_or_404(queryset, slug=slug)
        serializer = NewsDetailSerializer(instance)
        serializer.context['request'] = request
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def vote(self, request, *args, **kwargs):
        current_news = None

        value = request.GET.get('value', None)
        if value not in ['-1', '0', '1']:
            return Response(
                {'error': 'value должен быть равен -1, 0, или 1.'}, 400
            )

        current_user = request.user
        if isinstance(current_user, AnonymousUser):
            return Response({'message': 'Пожалуйста, авторизуйтесь.'}, 401)

        news_slug = kwargs.get('slug', None)
        if news_slug:
            current_news = Article.objects.filter(slug=news_slug).first()
        if not current_news:
            return Response({'error': 'Страница не найдена.'}, 404)

        user_rating = UserRatingsOfArticles.objects.filter(
            user=current_user, article=current_news)

        if not user_rating:
            UserRatingsOfArticles.objects.create(
                user=current_user, article=current_news, my_rating=value
            )

        return Response(
            {'message': 'Вы поставили Like.'}
        )


# class NewsViewSet(
#     mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
# ):
#     queryset = Article.objects.all()
#     serializer_class = NewsSerializer
#     pagination_class = NewsPagination
#     filter_backends = (filters.OrderingFilter,)
#     ordering_fields = ('rating', 'date_create',)
#     ordering = ('-rating',)
#     lookup_field = 'slug'
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = NewsDetailSerializer(instance)
#         return Response(serializer.data)
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
#         return Response(
#             {'message': 'Вы поставили Like.'}
#         )


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
