import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            Phone.objects.update_or_create(
                id=phone['id'],
                defaults={
                    'name': phone['name'],
                    'image': phone['image'],
                    'price': phone['price'],
                    'release_date': phone['release_date'],
                    'lte_exists': phone['lte_exists'] == 'True',
                }
            )
