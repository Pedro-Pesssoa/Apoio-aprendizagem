import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apoio_aprendizagem.perguntas.models import Conteudo
from apoio_aprendizagem.progresso.models import ProgressoUsuario
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestProgressoUsuarioAPI:

    def setup_method(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username="admin", password="123", is_staff=True)
        self.user = User.objects.create_user(username="aluno", password="123")
        self.conteudo = Conteudo.objects.create(nome="Condicionais", descricao="If/Else", modulo=1)

    def test_admin_can_create_progresso(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "usuario": self.user.id,
            "dados_progresso": {
                str(self.conteudo.id): {
                    "nivel_atual": "F",
                    "xp_acumulado": 0,
                    "perguntas_respondidas": []
                }
            }
        }
        response = self.client.post("/api/progressos/", data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "dados_progresso" in response.data

    def test_user_can_view_own_progresso(self):
        progresso = ProgressoUsuario.objects.create(
            usuario=self.user,
            dados_progresso={
                str(self.conteudo.id): {
                    "nivel_atual": "M",
                    "xp_acumulado": 30,
                    "perguntas_respondidas": [1, 2]
                }
            }
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/progressos/{progresso.id}/")
        assert response.status_code == status.HTTP_200_OK
        # Verifica se os dados sensíveis foram ocultados
        dados = response.data["dados_progresso"]
        for conteudo_id, progresso_data in dados.items():
            assert "nivel_atual" not in progresso_data
            assert "xp_acumulado" not in progresso_data
            assert "perguntas_respondidas" in progresso_data

    def test_admin_can_view_all_progress_data(self):
        progresso = ProgressoUsuario.objects.create(
            usuario=self.user,
            dados_progresso={
                str(self.conteudo.id): {
                    "nivel_atual": "M",
                    "xp_acumulado": 30,
                    "perguntas_respondidas": [1, 2]
                }
            }
        )
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/api/progressos/{progresso.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert "nivel_atual" in response.data["dados_progresso"][str(self.conteudo.id)]

    def test_user_can_list_only_own_progresso(self):
        progresso = ProgressoUsuario.objects.create(
            usuario=self.user,
            dados_progresso={
                str(self.conteudo.id): {
                    "nivel_atual": "F",
                    "xp_acumulado": 10,
                    "perguntas_respondidas": []
                }
            }
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/progressos/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["usuario"] == self.user.id

    def test_admin_can_delete_progresso(self):
        progresso = ProgressoUsuario.objects.create(usuario=self.user, dados_progresso={})
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/progressos/{progresso.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProgressoUsuario.objects.filter(id=progresso.id).exists()

    def test_user_cannot_delete_or_update(self):
        progresso = ProgressoUsuario.objects.create(usuario=self.user, dados_progresso={})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/progressos/{progresso.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = self.client.patch(f"/api/progressos/{progresso.id}/", data={"dados_progresso": {}}, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
