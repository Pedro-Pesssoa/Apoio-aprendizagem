from django.db import models
from .perguntas import Pergunta


class Alternativa(models.Model):
    """
    Model que descreve uma alternativa
    """
    pergunta = models.ForeignKey(
        Pergunta,
        on_delete=models.CASCADE,
        related_name='alternativas'
    )
    correta = models.BooleanField(default=False)
    texto = models.CharField(max_length=200)

    def __str__(self):
        return f"Alternativa {self.id} - {'Correta' if self.correta else 'Incorreta'}"
