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
            'title', 'preview', 'view_count', 'rating', 'date_create', 'url'
        )


class NewsDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор, используемый при отображении детальной информации о новости.
    """
    vote = serializers.HyperlinkedIdentityField(
        view_name='article-vote', lookup_field='slug')
    favorite = serializers.HyperlinkedIdentityField(
        view_name='article-favorite', lookup_field='slug')
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Article
        fields = '__all__'


class NewsAddSerializer(serializers.ModelSerializer):
    """Сериализатор, используемый при добавлении новости."""
    class Meta:
        model = Article
        fields = (
            'article_number', 'title', 'preview', 'content',
        )

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super(NewsAddSerializer, self).create(validated_data)
