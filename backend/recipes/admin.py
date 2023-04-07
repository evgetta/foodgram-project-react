from django.contrib.admin import (register, ModelAdmin)

from .models import (Recipe, Tag, Ingredient, AmountOfIngredients,
                     FavoritesList, ShoppingCart)

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
class LinksAdmin(ModelAdmin):
    pass


@register(FavoritesList)
class LinksAdmin(ModelAdmin):
    pass


@register(ShoppingCart)
class LinksAdmin(ModelAdmin):
    pass
