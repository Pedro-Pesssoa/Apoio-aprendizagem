from rest_framework import serializers
from ..models import Conteudo, Pergunta


class ConteudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conteudo
        fields = ['id', 'nome', 'modulo', 'descricao']


class PerguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pergunta
        fields = ['id', 'enunciado', 'imagem', 'nivel', 'alternativa_a', 'alternativa_b', 'alternativa_c', 'alternativa_d', 'alternativa_correta', 'conteudo']

    def to_representation(self, instance):
        """
        Personaliza a representação da pergunta para ajustar as alternativas
        se a pergunta for de nível fácil.
        """
        representation = super().to_representation(instance)

        # Se a pergunta for de nível fácil, ajusta as alternativas
        if instance.nivel == 'F':
            representation['alternativa_a'] = 'Verdadeiro'
            representation['alternativa_b'] = 'Falso'
            representation['alternativa_c'] = ''
            representation['alternativa_d'] = ''

        # Remove a resposta correta se o usuário não for staff
        request = self.context.get('request')
        if request and not request.user.is_staff:
            representation.pop('alternativa_correta', None)

        return representation
