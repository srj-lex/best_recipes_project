import csv

from django.core.management.base import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов'

    def load_ingredients(self):
        if Ingredient.objects.exists():
            return

        with open('../data/ingredients.csv', encoding='utf8') as file:
            data = csv.reader(file)
            for row in data:
                Ingredient.objects.create(
                    name=row[0],
                    measurement_unit=row[-1]
                )

    def handle(self, *args, **kwargs):
        self.load_ingredients()
