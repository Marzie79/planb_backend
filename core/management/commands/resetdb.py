import os
import glob
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Resets the database'

    def handle(self, *args, **options):
        dbname = settings.DATABASES["default"]["NAME"]

        cursor = connection.cursor()
        cursor.execute('show tables;')
        parts = ('DROP TABLE IF EXISTS %s;' % table for (table,) in cursor.fetchall())
        sql = 'SET FOREIGN_KEY_CHECKS = 0;\n' + '\n'.join(parts) + 'SET FOREIGN_KEY_CHECKS = 1;\n'
        connection.cursor().execute(sql)
        base = str(settings.BASE_DIR)
        migrations = glob.glob(os.path.join(base, "*", "migrations"))
        for migration in migrations:
            shutil.rmtree(migration)
        apps = [migration.split("\\")[-2] for migration in migrations]
        for app in apps:
            os.system("python manage.py makemigrations %s" % app)
        os.system("python manage.py migrate")