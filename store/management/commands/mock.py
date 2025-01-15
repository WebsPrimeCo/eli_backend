from django.core.management.base import BaseCommand
from store.factories import CategoryFactory, ProductFactory, CustomerFactory, OrderFactory

class Command(BaseCommand):
    help = 'Generate mock data for the database.'

    def add_arguments(self, parser):
        parser.add_argument('--categories', type=int, default=5)
        parser.add_argument('--products', type=int, default=20)
        parser.add_argument('--customers', type=int, default=10)
        parser.add_argument('--orders', type=int, default=15)

    def handle(self, *args, **kwargs):
        CategoryFactory.create_batch(kwargs['categories'])
        ProductFactory.create_batch(kwargs['products'])
        CustomerFactory.create_batch(kwargs['customers'])
        OrderFactory.create_batch(kwargs['orders'])
        self.stdout.write(self.style.SUCCESS('Mock data generated successfully!'))
