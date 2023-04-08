from csv import DictReader

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            with open('./data/ingredients.csv', 'r',
                      encoding='utf-8') as file:
                reader = DictReader(file)
                Ingredient.objects.bulk_create(
                    Ingredient(**data) for data in reader)
        except Exception:
            print('Ошибка загрузки')
        else:
            print('Загрузка завершена')
