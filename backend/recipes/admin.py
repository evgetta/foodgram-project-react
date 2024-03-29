from django.contrib.admin import ModelAdmin, register

from .models import (AmountOfIngredients, FavoritesList, Ingredient, Recipe,
                     ShoppingCart, Tag)

EMPTY_VALUE = 'Пустое значение'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = EMPTY_VALUE

    def count_favorites(self, obj):
        return obj.favorites.count()


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')
    empty_value_display = EMPTY_VALUE


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE


@register(AmountOfIngredients)
class AmountOfIngredientsAdmin(ModelAdmin):
    pass


@register(FavoritesList)
class FavoritesListAdmin(ModelAdmin):
    pass


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    pass
