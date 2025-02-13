from django.db import models
from .conteudos import Conteudo


class Pergunta(models.Model):
    """
    Model que descreve uma pergunta
    """
    NIVEL_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Médio'),
        ('D', 'Difícil'),
    ]

    conteudo = models.ForeignKey(
        Conteudo,
        on_delete=models.CASCADE,
        related_name='perguntas'
    )

    enunciado = models.TextField(
        verbose_name="Enunciado da questão"
    )

    imagem = models.ImageField(
        upload_to='perguntas/',
        null=True,
        blank=True,
        verbose_name="Imagem da questão"
    )

    nivel = models.CharField(
        max_length=1,
        choices=NIVEL_CHOICES,
        verbose_name="Nível da questão"
    )

    alternativa_a = models.CharField(
        max_length=200,
        verbose_name="Alternativa A"
    )

    alternativa_b = models.CharField(
        max_length=200,
        verbose_name="Alternativa B"
    )

    alternativa_c = models.CharField(
        max_length=200,
        verbose_name="Alternativa C"
    )

    alternativa_d = models.CharField(
        max_length=200,
        verbose_name="Alternativa D"
    )

    alternativa_correta = models.CharField(
        max_length=1,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D')
        ],
        verbose_name="Alternativa Correta"
    )

    def __str__(self):
        return f"{self.conteudo} - {self.id}"

    class Meta:
        """
        Define nomecletura da model
        """
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"
