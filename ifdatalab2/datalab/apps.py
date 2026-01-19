from django.apps import AppConfig
from django.db.models.signals import post_migrate

class DatalabConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'datalab'

    def ready(self):
        post_migrate.connect(criar_admin_padrao, sender=self)


def criar_admin_padrao(sender, **kwargs):
    from django.contrib.auth.models import User

    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@datalab.local",
            password="admin"
        )