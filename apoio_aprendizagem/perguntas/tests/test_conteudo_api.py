import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apoio_aprendizagem.models import Conteudo
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestConteudoAPI:

    def setup_method(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username="admin", password="123", is_staff=True)
        self.user = User.objects.create_user(username="aluno", password="123")

    def test_admin_can_create_conteudo(self):
        self.client.force_authenticate(user=self.admin)
        payload = {"nome": "Variáveis", "descricao": "Introdução a variáveis", "modulo": 1}
        response = self.client.post("/api/conteudos/", data=payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_cannot_create_conteudo(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/conteudos/", data={"nome": "Teste", "descricao": "desc", "modulo": 2})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authenticated_user_can_list_conteudos(self):
        Conteudo.objects.create(nome="Laços", descricao="Repetições", modulo=2)
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/conteudos/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_admin_can_update_conteudo(self):
        conteudo = Conteudo.objects.create(nome="Condicionais", descricao="If, else", modulo=1)
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(f"/api/conteudos/{conteudo.id}/", data={"nome": "Condicionais Atualizado"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nome"] == "Condicionais Atualizado"

    def test_user_cannot_delete_conteudo(self):
        conteudo = Conteudo.objects.create(nome="Cond", descricao="Teste", modulo=1)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/conteudos/{conteudo.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
