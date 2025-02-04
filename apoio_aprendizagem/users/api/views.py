import logging
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from apoio_aprendizagem.users.models import User
from .serializers import UserSerializer, PublicUserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    """
    ViewSet de usuario
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get_permissions(self):
        """
        Define as permissões com base na ação.
        """
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """
        Define qual serializer usar com base na ação e no usuário.
        """
        if self.action == "retrieve":
            return PublicUserSerializer
        return UserSerializer

    def get_queryset(self):
        """
        Define o queryset com base no tipo de usuário.
        """
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os detalhes de um usuário.
        """
        try:
            instance = self.get_object()

            if not request.user.is_staff and instance != request.user:
                return Response(
                    PublicUserSerializer(instance).data,
                    status=status.HTTP_200_OK
                )

            return Response(
                UserSerializer(instance).data,
                status=status.HTTP_200_OK
            )

        except Http404:
            raise NotFound("Usuário não encontrado.")

        except ValidationError:
            return Response(
                {"error": "ID inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.error(
                f"Erro inesperado ao buscar usuário: {str(e)}",
                exc_info=True)
            return Response(
                {"error": "Ocorreu um erro inesperado."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        """
        Atualiza um usuário.
        """
        instance = self.get_object()
        if not request.user.is_staff and instance != request.user:
            raise PermissionDenied("Você não tem permissão para editar este usuário.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Exclui um usuário.
        """
        instance = self.get_object()
        if not request.user.is_staff and instance != request.user:
            raise PermissionDenied("Você não tem permissão para excluir este usuário.")
        return super().destroy(request, *args, **kwargs)
