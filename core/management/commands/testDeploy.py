from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'run server on local ' \
           'makemigrations' \
           'migrate' \
           'pip install' \
           'runserver'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            'ip', nargs='?',
            help='ip and port',
        )

    # django-admin makemessages --locale=fa
    # or
    # django-admin makemessages --locale=fa --ignore=venv/*
    # django-admin compilemessages

    def handle(self, *args, **kwargs):
        try:
            # shellCommand = 'import subprocess;import sys;subprocess.run("pip install -r ' + settings.BASE_DIR.replace(
            #     '\\', '/') + '/requirements.txt");'
            # management.call_command('shell',
            #                         command=shellCommand)
            # management.call_command('dbbackup')
            management.call_command('makemessages', locale=['fa', ], ignore=['venv/*', ])
            management.call_command('compilemessages', locale=['fa', ], ignore=['venv/*', ])
            management.call_command('makemigrations')
            management.call_command('migrate')
            # management.call_command('collectstatic')
            # management.call_command('check','--deploy')
            # management.call_command('test')
            port = 'localhost:8000'
            if kwargs['ip']:
                port = kwargs['ip']
            management.call_command('runserver', port)

        except Exception as e:
            self.stdout.write(self.style.ERROR(print(e)))
