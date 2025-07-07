import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apoio_aprendizagem.models import Pergunta, Conteudo
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestPerguntaAPI:

    def setup_method(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username="admin", password="123", is_staff=True)
        self.user = User.objects.create_user(username="aluno", password="123")
        self.conteudo = Conteudo.objects.create(nome="Funções", descricao="def, return", modulo=2)

    def criar_pergunta(self, nivel="M"):
        return Pergunta.objects.create(
            conteudo=self.conteudo,
            enunciado="Qual o resultado de 2+2?",
            nivel=nivel,
            alternativa_a="1",
            alternativa_b="2",
            alternativa_c="3",
            alternativa_d="4",
            alternativa_correta="D"
        )

    def test_admin_can_create_pergunta(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "conteudo": self.conteudo.id,
            "enunciado": "Teste?",
            "nivel": "F",
            "alternativa_a": "V",
            "alternativa_b": "F",
            "alternativa_c": "",
            "alternativa_d": "",
            "alternativa_correta": "A"
        }
        response = self.client.post("/api/perguntas/", data=payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_cannot_create_pergunta(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "conteudo": self.conteudo.id,
            "enunciado": "Teste",
            "nivel": "M",
            "alternativa_a": "1",
            "alternativa_b": "2",
            "alternativa_c": "3",
            "alternativa_d": "4",
            "alternativa_correta": "B"
        }
        response = self.client.post("/api/perguntas/", data=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_can_list_perguntas_without_ver_gabarito(self):
        pergunta = self.criar_pergunta()
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/perguntas/")
        assert response.status_code == status.HTTP_200_OK
        assert all("alternativa_correta" not in p for p in response.data)

    def test_admin_sees_alternativa_correta(self):
        pergunta = self.criar_pergunta()
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/perguntas/")
        assert response.status_code == status.HTTP_200_OK
        assert "alternativa_correta" in response.data[0]

    def test_facil_pergunta_alternativas_true_false(self):
        pergunta = self.criar_pergunta(nivel="F")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/perguntas/{pergunta.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["alternativa_a"] == "Verdadeiro"
        assert response.data["alternativa_b"] == "Falso"

    def test_responder_pergunta_certa(self):
        pergunta = self.criar_pergunta()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/perguntas/{pergunta.id}/responder/", data={"resposta": "D"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["correto"] is True

    def test_responder_pergunta_errada(self):
        pergunta = self.criar_pergunta()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/perguntas/{pergunta.id}/responder/", data={"resposta": "A"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["correto"] is False
