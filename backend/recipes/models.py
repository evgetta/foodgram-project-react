from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='image_recipes/',
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='AmountOfIngredients',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(1, 'Время приготовления не менее 1 минуты'),
            MaxValueValidator(1440, 'Время приготовления не более суток')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Наименование тега',
        max_length=64,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=8,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг тэга',
        max_length=64,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Наименование ингредиента',
        max_length=64
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=32
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class AmountOfIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients_amount',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredients_amount',
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Количество ингредиентов не менее 1')
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}'


class FavoritesList(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        verbose_name='Избранный рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='cart',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_user'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe.name}'
