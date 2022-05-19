from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'article_number', 'title', 'author', 'slug', 'summary',
        'content', 'view_count', 'rating',
    )
    ordering = ('id',)
    list_display_links = ('id', 'title',)
