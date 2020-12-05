from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class AccountConfig(AppConfig):
    name = 'accounts'
    verbose_name = gettext_lazy("accounts")

    def ready(self):
        import core.signals
