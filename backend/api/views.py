from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import HttpResponse
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        SAFE_METHODS)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import (Ingredient, Recipe, Tag, FavoritesList, 
                            AmountOfIngredients,
                            ShoppingCart)
from .serializers import (SubscriptionSerializer,
                          CheckSubscribeSerializer,
                          TagSerializer, IngredientSerializer,
                          RecipeCreateSerializer,
                          RecipeListSerializer, FavoritesListSerializer,
                          ShoppingCartSerializer)
from .mixins import ListRetrieveViewSet
from .permissions import IsAdminOrReadOnly, IsAdminAuthorOrReadOnly
from .paginations import PageNumberPaginationLimit
from .filters import IngredientFilter, RecipeFilter

from users.models import Subscription

User = get_user_model()


class SubscriptionViewSet(UserViewSet):
    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    @transaction.atomic()
    def subscribe(self, request, id=None):

        user = request.user
        author = get_object_or_404(User, pk=id)
        data = {
            'user': user.id,
            'author': author.id,
        }
        serializer = CheckSubscribeSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        result = Subscription.objects.create(user=user, author=author)
        serializer = SubscriptionSerializer(
            result, context={'request': request})
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @subscribe.mapping.delete
    @transaction.atomic()
    def del_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        data = {
            'user': user.id,
            'author': author.id,
        }
        serializer = CheckSubscribeSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user.subscriber.filter(author=author).delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = user.subscriber.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
   
    
class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filter_class = IngredientFilter
 

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipeListSerializer
    permission_classes = (IsAdminAuthorOrReadOnly,)
    pagination_class = PageNumberPaginationLimit
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAdminAuthorOrReadOnly])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if FavoritesList.objects.filter(user=user, 
                                            recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = FavoritesList.objects.create(
                user=user, recipe=recipe)
            serializer = FavoritesListSerializer(
                favorite, context={'request': request})
            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = FavoritesList.objects.filter(user=user, 
                                                    recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAdminAuthorOrReadOnly])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, 
                                           recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            shoping_cart = ShoppingCart.objects.create(user=user,
                                                       recipe=recipe)
            serializer = ShoppingCartSerializer(
                shoping_cart, context={'request': request})
            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            delete_shoping_cart = ShoppingCart.objects.filter(
                user=user, recipe=recipe)
            if delete_shoping_cart.exists():
                delete_shoping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, 
        methods=['GET'],
        permission_classes=[IsAdminAuthorOrReadOnly])
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        filename = f'{user.username}_shoppingcart.txt'
        shoppingcart = [
            f'Список покупок для:\n\n{user.first_name}\n'
        ]
        ingredients = AmountOfIngredients.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=Sum('amount'))
        shoppingcart += '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["total"]}/'
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
        response = HttpResponse(shoppingcart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
