from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create schema if not present and insert seed data'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("CREATE SCHEMA IF NOT EXISTS ahj_schema;")
            self.stdout.write(self.style.SUCCESS('AHJ schema created successfully'))
