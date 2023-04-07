from django.core.management import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#02BCFA', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#FA5102', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#2E243B', 'slug': 'dinner'},
        ]
        try:
            Tag.objects.bulk_create(Tag(**tag) for tag in data)
        except Exception:
            print('Ошибка загрузки')
        else:
            print('Загрузка завершена')
