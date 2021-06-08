from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'run test with covrage '

    def handle(self, *args, **kwargs):
        try:
            test_command = 'import subprocess;import sys;import os;'\
                           'subprocess.run("coverage run manage.py test ");'\
                           'subprocess.run("coverage html");'\
                           'subprocess.Popen("start microsoft-edge:http://localhost:8000/",shell = True);'\
                           'os.chdir("htmlcov");subprocess.run("python -m http.server");'
            management.call_command('shell', command=test_command)
        except Exception as e:
            self.stdout.write(self.style.ERROR(print(e)))
