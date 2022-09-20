from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
	# Campos de leitura
		readonly_fields = ()

	# Campos de edição
		fieldsets = (
				("Credentials", {"fields" : ("username", "password")}),
				("Permissions", {"fields" : ("is_superuser","is_owner",)}),
		)

	# Colunas da Tabela de Filtro
		list_display = ("username", "is_superuser")

admin.site.register(User, CustomUserAdmin)
