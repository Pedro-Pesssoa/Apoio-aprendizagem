from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from apoio_aprendizagem.users.api.views import UserViewSet
from apoio_aprendizagem.perguntas.api.views import PerguntaViewSet, ConteudoViewSet
from apoio_aprendizagem.progressos.api.views import ProgressoUsuarioViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("perguntas", PerguntaViewSet)
router.register("conteudos", ConteudoViewSet)
router.register("progresso", ProgressoUsuarioViewSet)

app_name = "api"
urlpatterns = router.urls
