from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProgressoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apoio_aprendizagem.progressos'
    verbose_name = _("Progressos")
