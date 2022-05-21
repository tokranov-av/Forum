from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.reverse import reverse

User = get_user_model()


class Article(models.Model):
    article_number = models.PositiveIntegerField(
        db_index=True, verbose_name='Артикул')
    title = models.CharField(max_length=55, verbose_name='Заголовок',)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор поста')
    slug = models.SlugField(max_length=55, unique=True)
    summary = models.CharField(
        max_length=250, verbose_name='Краткое содержание')
    content = models.TextField(verbose_name='Содержание')
    view_count = models.PositiveIntegerField(
        verbose_name='Количество просмотров', default=0)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    date_create = models.DateField(
        auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['id']


class UserRatingsOfArticles(models.Model):
    VALUE_RATING = (
        ('-1', 'Отрицательно'),
        ('0', 'Нейтрально'),
        ('1', 'Положительно'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='user_ratings',
        verbose_name='Статья'
    )
    rating = models.CharField(
        max_length=20, choices=VALUE_RATING, default='0',
        verbose_name='Рейтинг'
    )
    in_favorites = models.BooleanField(
        default=False, verbose_name='В избранном')

    class Meta:
        verbose_name = 'Пользовательские рейтинги'
        verbose_name_plural = 'Пользовательские рейтинги'
        ordering = ['id']
