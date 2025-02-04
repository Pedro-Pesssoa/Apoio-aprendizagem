from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Força o processo de login do admin a usar o workflow do `django-allauth`
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # Campos exibidos na lista de usuários
    list_display = [
        "username", "name", "email", "instituicao", "escolaridade", "ativo", "is_staff"
    ]

    # Campos pesquisáveis na lista de usuários
    search_fields = ["username", "name", "email", "instituicao"]

    # Filtros laterais
    list_filter = ["ativo", "is_staff", "escolaridade"]

    # Campos exibidos no formulário de edição
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Informações Pessoais"), {
            "fields": (
                "name", "email", "avatar", "instituicao", "data_nascimento", "escolaridade"
            ),
        }),
        (_("Permissões"), {
            "fields": (
                "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
            ),
        }),
        (_("Datas Importantes"), {
            "fields": ("last_login", "data_criacao", "data_atualizacao")
        }),
    )

    # Campos exibidos no formulário de criação
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password2", "name", "email", "instituicao",
                "data_nascimento", "escolaridade", "is_active", "is_staff", "is_superuser"
            ),
        }),
    )

    # Campos somente leitura (não editáveis)
    readonly_fields = ["data_criacao", "data_atualizacao", "last_login"]