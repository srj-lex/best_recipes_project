import csv

from django.core.management.base import BaseCommand

from recipe.models import Ingridient


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов'

    def load_ingridients(self):
        with open('../../data/ingredients.csv', encoding='utf8') as file:
            data = csv.reader(file)
            for row in data:
                Ingridient.objects.create(
                    name=row[0],
                    measurement_unit=row[-1]
                )
        print('Ингридиенты загружены')

    def handle(self, *args, **kwargs):
        self.load_ingridients()
