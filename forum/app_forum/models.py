from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Article(models.Model):
    article_number = models.PositiveIntegerField(
        db_index=True, verbose_name='Артикул')
    title = models.CharField(max_length=55, verbose_name='Заголовок')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор поста')
    slug = models.SlugField(max_length=55)
    summary = models.CharField(
        max_length=250, verbose_name='Краткое содержание')
    content = models.TextField(verbose_name='Содержание')
    view_count = models.PositiveIntegerField(
        verbose_name='Количество просмотров', default=0)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['id']


class UserRatingsOfArticles(models.Model):
    VALUE_RATING = (
        (-1, 'Отрицательно'),
        (0, 'Нейтрально'),
        (1, 'Положительно'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='Статья')
    my_rating = models.CharField(max_length=20, choices=VALUE_RATING)
    in_favorites = models.BooleanField(
        default=False, verbose_name='В избранном')

    class Meta:
        verbose_name = 'Р'
        verbose_name_plural = 'Категории'
        ordering = ['id']
