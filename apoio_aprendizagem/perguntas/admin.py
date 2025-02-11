from django.contrib import admin
from .models import Pergunta, Conteudo


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'nivel', 'conteudo', 'alternativa_correta')
    list_filter = ('nivel', 'conteudo')
    search_fields = ('enunciado',)
    fieldsets = (
        (None, {
            'fields': ('enunciado', 'imagem', 'nivel', 'conteudo')
        }),
        ('Alternativas', {
            'fields': (
                ('alternativa_a', 'alternativa_b'),
                ('alternativa_c', 'alternativa_d'),
                'alternativa_correta'
            ),
        }),
    )


@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    """
    Admin para o model Conteudo.
    """
    list_display = ('nome', 'modulo', 'descricao_curta')

    def descricao_curta(self, obj):
        """
        Retorna uma versão curta da descrição para exibição no admin.
        """
        return f"{obj.descricao[:50]}..." if len(obj.descricao) > 50 else obj.descricao
    descricao_curta.short_description = "Descrição"
