from rest_framework import serializers
from .models import ProgressoUsuario

class ProgressoUsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo ProgressoUsuario.
    """

    class Meta:
        model = ProgressoUsuario
        fields = ['usuario', 'dados_progresso']

    def to_representation(self, instance):
        """
        Personaliza a representação dos dados de progresso.
        Para usuários comuns, remove informações sensíveis como nível atual e XP acumulado.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Se o usuário não for administrador, remova detalhes sensíveis
        if not request.user.is_staff:
            sanitized_progress_data = {}
            for conteudo_id, progress in instance.dados_progresso.items():
                sanitized_progress_data[conteudo_id] = {
                    "perguntas_respondidas": progress.get("perguntas_respondidas", []),
                }
            representation['dados_progresso'] = sanitized_progress_data

        return representation

    def validate(self, data):
        """
        Validação personalizada para garantir que o JSONField esteja no formato correto.
        """
        dados_progresso = data.get('dados_progresso', {})
        for conteudo_id, progress in dados_progresso.items():
            required_keys = {"nivel_atual", "xp_acumulado", "perguntas_respondidas"}
            if not required_keys.issubset(progress.keys()):
                raise serializers.ValidationError(
                    f"Os campos 'nivel_atual', 'xp_acumulado' e 'perguntas_respondidas' são obrigatórios para o conteúdo {conteudo_id}."
                )
        return data