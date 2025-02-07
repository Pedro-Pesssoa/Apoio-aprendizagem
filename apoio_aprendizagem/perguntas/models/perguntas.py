from django.db import models
from .conteudos import Conteudo


class Pergunta(models.Model):
    """
    Model que descreve uma pergunta
    """
    NIVEL_CHOICES = (
        ('F', 'Fácil'),
        ('M', 'Médio'),
        ('D', 'Difícil')
    )

    conteudo = models.ForeignKey(
        Conteudo,
        on_delete=models.CASCADE,
        related_name='perguntas'
    )
    nivel = models.CharField(
        max_length=1,
        choices=NIVEL_CHOICES
    )
    texto = models.TextField()
    imagem = models.ImageField(
        upload_to='perguntas/imagens/',
        blank=True,
        null=True
    )
    experiencia = models.FloatField()

    def __str__(self):
        return f"Pergunta {self.conteudo} - {self.id}"
