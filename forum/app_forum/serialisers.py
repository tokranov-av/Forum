from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app_forum.models import Article

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор, используемый при регистрации пользователей."""
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def validate_password(self, value: str) -> str:
        """Хеширование пароля."""
        return make_password(value)


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор, используемый при отображении новостей."""
    url = serializers.HyperlinkedIdentityField(
        view_name='article-detail', lookup_field='slug')

    class Meta:
        model = Article
        fields = (
            'title', 'summary', 'view_count', 'rating', 'date_create', 'url'
        )


class NewsDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор, используемый при отображении детальной информации о новости.
    """
    vote = serializers.HyperlinkedIdentityField(
        view_name='article-vote', lookup_field='slug')

    class Meta:
        model = Article
        fields = '__all__'


# class NewsCreateSerializer(serializers.ModelSerializer):
#     """Сериализатор, используемый при отображении новостей."""
#     class Meta:
#         model = Article
#         fields = ('article_number', 'title', 'slug', 'summary', 'content')
