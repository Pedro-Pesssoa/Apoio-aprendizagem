import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Model base de usuario.
    """
    ESCOLARIDADE_CHOICES = [
        ('fundamental_incompleto', 'Fundamental Incompleto'),
        ('fundamental_completo', 'Fundamental Completo'),
        ('medio_incompleto', 'Ensino Médio Incompleto'),
        ('medio_completo', 'Ensino Médio Completo'),
        ('superior_incompleto', 'Ensino Superior Incompleto'),
        ('superior_completo', 'Ensino Superior Completo'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        _("Nome do usuario"),
        blank=True,
        max_length=255
    )
    avatar = models.ImageField(
        _("Avatar"),
        upload_to="avatars/",
        blank=True,
        null=True
    )
    instituicao = models.CharField(
        _("Instituicao"),
        max_length=255,
        blank=True
    )
    data_nascimento = models.DateField(
        _("Data de Nascimento"),
        blank=True,
        null=True
    )
    ativo = models.BooleanField(
        _("Usuario ativo"),
        default=False
    )
    escolaridade = models.CharField(
        _("Escolaridade"),
        max_length=22,
        choices=ESCOLARIDADE_CHOICES,
        blank=True,
        null=True,
    )
    data_criacao = models.DateTimeField(
        _("Data de Criação"),
        auto_now_add=True
    )
    data_atualizacao = models.DateTimeField(
        _("Data de Edição"),
        auto_now=True
    )

    def __str__(self):
        return f'${self.username}'

    def get_absolute_url(self) -> str:
        """ Retorna a URL do detalhe do usuário. """
        return reverse("users:detail", kwargs={"username": self.username})
