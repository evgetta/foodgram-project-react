from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='subscribing',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='subscriber',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'Подписчик {self.user.username} на автора {self.author.username}'
