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
        if 'db.sqlite3' in dbname:
            pass
            # try:
            #     f = open("delete_data.sql", "r", encoding='UTF-8')
            #     sql = f.read()
            #     cursor.executescript(sql)
            # except:
            #     print("not_Deletd")
        else:
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
        # if 'db.sqlite3' in dbname:
        f = open("test_data.sql", "r", encoding='UTF-8')
        sql = f.read()
        cursor.executescript(sql)
        # cursor.executescript(sql)

    # def delete_all_tables(self, cursor):
    #     tables = self.get_tables(cursor)
    #     print(tables)
    #     self.delete_tables(cursor, tables)
    #
    # def get_tables(self, cursor):
    #     cursor.execute("SELECT name FROM sqlite_schema WHERE type='table';")
    #     tables = cursor.fetchall()
    #     return tables
    #
    # def delete_tables(self, cursor, tables):
    #     TABLE_PARAMETER = "{TABLE_PARAMETER}"
    #     for table, in tables:
    #         sql = f"DROP TABLE {TABLE_PARAMETER};".replace("SELECT name FROM sqlite_schema WHERE type='table';", table)
    #         cursor.execute(sql)
