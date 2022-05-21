from rest_framework.generics import CreateAPIView
from rest_framework import filters
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from .models import Article, UserRatingsOfArticles
from .serialisers import (
    RegistrationSerializer, NewsSerializer, NewsDetailSerializer,
    NewsAddSerializer
)
from django.contrib.auth import get_user_model
from .pagination import NewsPagination
from .filters import FavoritesFilter
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class RegistrationAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class NewsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter, FavoritesFilter)
    ordering_fields = ('rating', 'date_create',)
    ordering = ('-rating',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = NewsDetailSerializer(instance)
        instance.view_count += 1
        instance.save(update_fields=['view_count', ])
        serializer.context['request'] = request
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def vote(self, request, *args, **kwargs):

        value = request.GET.get('value', None)
        if value not in ['-1', '0', '1']:
            return Response(
                {'error': 'value должен быть равен -1, 0, или 1.'}, 400
            )
        current_news = self.get_object()
        current_user = request.user
        message = 'Оценка не изменилась'

        user_rating = UserRatingsOfArticles.objects.filter(
            user=current_user, article=current_news).first()

        if not user_rating:
            UserRatingsOfArticles.objects.create(
                user=current_user, article=current_news, rating=value)

            if value != '0':
                if value == '-1':
                    current_news.rating -= 1
                    message = 'Вы поставили Dislike!'
                elif value == '1':
                    current_news.rating += 1
                    message = 'Вы поставили Like!'
                current_news.save(update_fields=['rating'])

        elif user_rating.rating != value:

            if value == '-1':
                if user_rating.rating == '0':
                    current_news.rating -= 1
                if user_rating.rating == '1':
                    current_news.rating -= 2
                message = 'Вы поставили Dislike!'
            elif value == '1':
                if user_rating.rating == '0':
                    current_news.rating += 1
                if user_rating.rating == '-1':
                    current_news.rating += 2
                message = 'Вы поставили Like!'
            else:
                if user_rating.rating == '-1':
                    current_news.rating += 1
                elif user_rating.rating == '1':
                    current_news.rating -= 1
                message = 'Вы удалили оценку.'

            user_rating.rating = value
            user_rating.save(update_fields=['rating'])
            current_news.save(update_fields=['rating'])

        return Response(
            {'message': message}, 200
        )

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, *args, **kwargs):

        value = request.GET.get('value', None)
        if value not in ['add', 'remove']:
            return Response(
                {'error': 'value должен быть равен "add" или "remove".'}, 400
            )
        if value == 'add':
            favorite = True
            message = 'Вы добавили статью в "Избранное"!'
        else:
            favorite = False
            message = 'Вы убрали статью из "Избранных"!'

        current_news = self.get_object()
        current_user = request.user

        user_data = UserRatingsOfArticles.objects.filter(
            user=current_user, article=current_news).first()

        if not user_data:
            UserRatingsOfArticles.objects.create(
                user=current_user, article=current_news, in_favorites=favorite)
        elif user_data.in_favorites != favorite:
            user_data.in_favorites = favorite
            user_data.save(update_fields=['in_favorites'])
        else:
            if favorite:
                message = 'Статья была ранее добавлена в "Избранное"'
            else:
                message = 'Статья не была в "Избранных"'

        return Response(
            {'message': message}, 200
        )


class AddNewsAPIView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = NewsAddSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
