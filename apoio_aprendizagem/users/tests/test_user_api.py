import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apoio_aprendizagem.users.models import User

@pytest.mark.django_db
class TestUserAPI:

    def setup_method(self):
        self.client = APIClient()

    def test_create_user(self):
        payload = {
            "username": "novo_usuario",
            "password": "senha123",
            "name": "Novo Usuário",
            "instituicao": "UFERSA",
        }
        response = self.client.post("/api/users/", data=payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert "password" not in response.data

    def test_public_user_retrieve(self, django_user_model):
        user = django_user_model.objects.create_user(username="usuario_pub", password="123")
        response = self.client.get(f"/api/users/{user.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert "name" in response.data
        assert "avatar" in response.data
        assert "instituicao" in response.data
        assert "username" not in response.data

    def test_authenticated_user_retrieve(self, django_user_model):
        user = django_user_model.objects.create_user(username="usuario_priv", password="123", name="Privado")
        self.client.force_authenticate(user=user)
        response = self.client.get(f"/api/users/{user.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Privado"
        assert "username" in response.data

    def test_update_own_user(self, django_user_model):
        user = django_user_model.objects.create_user(username="user_up", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.patch(f"/api/users/{user.id}/", data={"name": "Nome Atualizado"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Nome Atualizado"

    def test_update_other_user_forbidden(self, django_user_model):
        user1 = django_user_model.objects.create_user(username="user1", password="123")
        user2 = django_user_model.objects.create_user(username="user2", password="123")
        self.client.force_authenticate(user=user1)
        response = self.client.patch(f"/api/users/{user2.id}/", data={"name": "Hack"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_own_user(self, django_user_model):
        user = django_user_model.objects.create_user(username="user_del", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.delete(f"/api/users/{user.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user.id).exists()

    def test_delete_other_user_forbidden(self, django_user_model):
        user1 = django_user_model.objects.create_user(username="user1", password="123")
        user2 = django_user_model.objects.create_user(username="user2", password="123")
        self.client.force_authenticate(user=user1)
        response = self.client.delete(f"/api/users/{user2.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_requires_authentication(self):
        response = self.client.get("/api/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
