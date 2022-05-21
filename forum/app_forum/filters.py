from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import AnonymousUser


class FavoritesFilter(DjangoFilterBackend):
    """Фильтрация избранных новостей."""
    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)
        favorites = request.query_params.get('favorites')
        liked = request.query_params.get('liked')

        user = request.user
        if favorites == 'True' and not isinstance(user, AnonymousUser):
            queryset = queryset.filter(
                user_ratings__in_favorites=True,
                user_ratings__user=user
            )
        if liked == 'True' and not isinstance(user, AnonymousUser):
            queryset = queryset.filter(
                user_ratings__rating='1',
                user_ratings__user=user
            )
        return queryset
