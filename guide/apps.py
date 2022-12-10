from django.apps import AppConfig
import os


class GuideConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "guide"

    def ready(self):
        from django.contrib.auth.views import PasswordResetView
        PasswordResetView.from_email = os.environ['EMAIL_FROM']
