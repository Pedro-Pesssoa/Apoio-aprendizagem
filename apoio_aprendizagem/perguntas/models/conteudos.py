from django.db import models


class Conteudo(models.Model):
    """
    Model que descreve um conteudo
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    modulo = models.IntegerField()

    def __str__(self):
        return f"{self.nome} (Módulo {self.modulo})"
