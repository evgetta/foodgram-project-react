from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (SubscriptionViewSet,
                    IngredientViewSet, RecipeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', SubscriptionViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
