from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Conteudo, Pergunta
from .serializers import ConteudoSerializer, PerguntaSerializer


class ConteudoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Conteúdo.
    Apenas administradores podem criar, atualizar ou excluir conteúdos.
    Qualquer usuário autenticado pode visualizar conteúdos.
    """
    queryset = Conteudo.objects.all()
    serializer_class = ConteudoSerializer

    def get_permissions(self):
        """
        Define permissões personalizadas para cada ação.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class PerguntaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Perguntas.
    Apenas administradores podem criar, atualizar ou excluir perguntas.
    Qualquer usuário autenticado pode visualizar perguntas e validar respostas.
    """
    queryset = Pergunta.objects.all()
    serializer_class = PerguntaSerializer

    def get_permissions(self):
        """
        Define permissões personalizadas para cada ação.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def responder(self, request, pk=None):
        """
        Endpoint para validar a resposta do usuário.
        Qualquer usuário autenticado pode usar este endpoint.
        """
        pergunta = self.get_object()
        resposta_usuario = request.data.get('resposta', '').upper()

        # Verifica se a resposta do usuário está correta
        if resposta_usuario == pergunta.alternativa_correta:
            return Response({"correto": True}, status=status.HTTP_200_OK)
        else:
            return Response({"correto": False}, status=status.HTTP_200_OK)
