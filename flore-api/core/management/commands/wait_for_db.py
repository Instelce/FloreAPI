"""
Django command to wait for the database to be available
"""

import time

from psycopg2 import OperationalError as Psycopg2OperationError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        db_up = False

        self.stdout.write("Waiting for database")

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OperationError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second ...")
                time.sleep(1)

        self.stdout.write("Database available")