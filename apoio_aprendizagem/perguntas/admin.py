from django.contrib import admin
from .models import Alternativa, Pergunta, Conteudo


class AlternativaInline(admin.TabularInline):
    """
    Inline para exibir Alternativa dentro de Pergunta no painel admin.
    """
    model = Alternativa
    extra = 4
    min_num = 2
    max_num = 4


@admin.register(Alternativa)
class AlternativaAdmin(admin.ModelAdmin):
    """
    Admin para o model Alternativa.
    """
    list_display = ('texto', 'pergunta', 'correta')
    list_editable = ('correta',)
    search_fields = ('texto',)


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    """
    Admin para o model Pergunta.
    """
    inlines = [AlternativaInline]
    list_display = ('texto', 'conteudo', 'nivel', 'experiencia')
    list_filter = ('conteudo', 'nivel')
    search_fields = ('texto',)


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
