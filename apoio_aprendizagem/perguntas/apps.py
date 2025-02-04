from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PerguntasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apoio_aprendizagem.perguntas'
    verbose_name = _("Perguntas")
