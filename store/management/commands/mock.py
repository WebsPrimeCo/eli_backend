from django.core.management.base import BaseCommand
from faker import Faker
from myapp.models import YourModel  # مدل‌هایی که می‌خواهی داده بسازی

fake = Faker()

class Command(BaseCommand):
    help = 'Generate mock data for the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of mock records to create.'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        for _ in range(count):
            YourModel.objects.create(
                name=fake.name(),
                email=fake.email(),
                address=fake.address(),
                phone_number=fake.phone_number(),
                created_at=fake.date_time_this_year(),
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} mock records!'))
