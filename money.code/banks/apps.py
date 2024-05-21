from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class BanksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banks'

    def ready(self):
        from .views import update_value_date, periodic_ops
        user_logged_in.connect( update_value_date )
        user_logged_in.connect( periodic_ops )
