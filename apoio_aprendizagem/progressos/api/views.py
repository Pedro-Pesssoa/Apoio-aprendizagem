from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import ProgressoUsuario
from .serializers import ProgressoUsuarioSerializer
from django.shortcuts import get_object_or_404


class ProgressoUsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações relacionadas ao progresso do usuário.
    - Criação automática de progresso após cadastro.
    - Visualização de progresso por usuários ou administradores.
    - Edição de progresso por administradores.
    - Exclusão de progresso ao deletar um usuário.
    - Listagem de progresso de um usuário.
    """
    queryset = ProgressoUsuario.objects.all()
    serializer_class = ProgressoUsuarioSerializer

    def get_permissions(self):
        """
        Define permissões com base na ação.
        - Usuários autenticados podem visualizar seu próprio progresso.
        - Administradores podem criar, editar e excluir progressos.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Cria automaticamente o progresso de um usuário após o cadastro.
        """
        user = self.request.user
        serializer.save(usuario=user)

    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os detalhes do progresso de um usuário.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Lista todos os progressos de um usuário.
        """
        user = request.user
        progresso = get_object_or_404(ProgressoUsuario, usuario=user)
        serializer = self.get_serializer(progresso)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Exclui o progresso de um usuário.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)