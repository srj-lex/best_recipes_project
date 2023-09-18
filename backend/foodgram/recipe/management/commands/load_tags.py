import csv

from django.core.management.base import BaseCommand

from recipe.models import Tag


class Command(BaseCommand):
    help = 'Импорт тэгов из csv файла.'

    def load_tags(self):
        if Tag.objects.exists():
            return

        with open('../data/tags.csv', encoding='utf8') as file:
            data = csv.reader(file)
            for row in data:
                Tag.objects.create(
                    name=row[0],
                    measurement_unit=row[-1]
                )

    def handle(self, *args, **kwargs):
        self.load_tags()
