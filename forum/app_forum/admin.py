from django.contrib import admin
from .models import Article, UserRatingsOfArticles


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'article_number', 'title', 'author', 'slug', 'preview',
        'content', 'view_count', 'rating', 'date_create',
    )
    ordering = ('id',)
    list_display_links = ('id', 'title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(UserRatingsOfArticles)
class UserRatingsOfArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'article', 'rating', 'in_favorites', )
    ordering = ('id',)
    list_display_links = ('id', 'article',)
    list_filter = ('in_favorites', 'rating',)

