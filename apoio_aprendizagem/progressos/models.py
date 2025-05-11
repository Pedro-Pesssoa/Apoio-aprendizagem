from django.db import models
from django.contrib.auth import get_user_model
from apoio_aprendizagem.perguntas.models import Conteudo

User = get_user_model()


class ProgressoUsuario(models.Model):
    """
    Modelo que rastreia o progresso de um usuário em um conteúdo específico.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='progresso',
        verbose_name="Usuário"
    )

    dados_progresso = models.JSONField(
        default=dict,
        verbose_name="Dados de Progresso"
    )

    def __str__(self):
        return f"Progresso de {self.usuario.username}"

    class Meta:
        """
        Define nomecletura da model
        """
        verbose_name = "Progresso do Usuário"
        verbose_name_plural = "Progressos dos Usuários"

    def registrar_progresso(self, conteudo_id, pergunta_id, xp_ganho):
        """
        Registra o progresso do usuário após responder uma pergunta.
        Atualiza o nível, XP e lista de perguntas respondidas para o
        conteúdo específico.
        """

        if str(conteudo_id) not in self.dados_progresso:
            self.dados_progresso[str(conteudo_id)] = {
                "nivel_atual": "F",
                "xp_acumulado": 0,
                "perguntas_respondidas": []
            }

        conteudo_progresso = self.dados_progresso[str(conteudo_id)]
        conteudo_progresso["xp_acumulado"] += xp_ganho
        conteudo_progresso["perguntas_respondidas"].append(pergunta_id)

        if conteudo_progresso["xp_acumulado"] >= 45:
            conteudo_progresso["nivel_atual"] = "D"
        elif conteudo_progresso["xp_acumulado"] >= 30:
            conteudo_progresso["nivel_atual"] = "M"
        else:
            conteudo_progresso["nivel_atual"] = "F"

        # Salva as alterações
        self.save()

    def verificar_pergunta_respondida(self, conteudo_id, pergunta_id):
        """
        Verifica se o usuário já respondeu a uma pergunta específica de um conteúdo.
        Retorna True se a pergunta já foi respondida, False caso contrário.
        """
        conteudo_progresso = self.dados_progresso.get(str(conteudo_id), {})
        perguntas_respondidas = conteudo_progresso.get("perguntas_respondidas", [])
        return pergunta_id in perguntas_respondidas
