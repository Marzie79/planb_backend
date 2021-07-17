import os

from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'run server on local ' \
           'makemigrations' \
           'migrate' \
           'pip install' \
           'runserver'

    def add_arguments(self, parser):
        parser.add_argument(
            'ip', nargs='?',
            help='ip and port',
        )

    def handle(self, *args, **kwargs):
        try:
            management.call_command('makemessages', locale=['fa', ], ignore=['venv/*', ], *['--no-location'])
            management.call_command('compilemessages', locale=['fa', ], ignore=['venv/*', ])
            os.system("python manage.py resetdb")
            port = 'localhost:8000'

            management.call_command('runserver', port,'--noreload')

        except Exception as e:
            self.stdout.write(self.style.ERROR(print(e)))
