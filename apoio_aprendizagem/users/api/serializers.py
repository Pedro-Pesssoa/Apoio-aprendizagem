from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from apoio_aprendizagem.users.models import User


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer para visualização pública de um
    usuário (nome, avatar, instituição).
    """
    class Meta:
        model = User
        fields = ["name", "avatar", "instituicao"]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para visualização completa de um
    usuário (exceto dados de sistema).
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "name", "avatar", "instituicao",
            "data_nascimento", "ativo", "escolaridade", "data_criacao",
            "data_atualizacao", "password"
        ]
        read_only_fields = ["data_criacao", "data_atualizacao"]

        def create(self, validated_data):
            """
            Cria um novo usuário com a senha hash.
            """
            # Extrai a senha do validated_data
            password = validated_data.pop("password")
            # Cria o usuário com a senha hash
            user = User(**validated_data)
            user.set_password(password)  # Aplica o hash na senha
            user.save()
            return user

    def update(self, instance, validated_data):
        """
        Atualiza um usuário existente.
        """
        # Se a senha for fornecida, aplica o hash
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        # Atualiza os outros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
