
from django.contrib import admin
from .models import Livro, Leitor, Emprestimo


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "autor",
        "genero",
        "quantidade_total",
        "quantidade_disponivel",
    )
    search_fields = ("titulo", "autor")


@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "email")
    search_fields = ("nome",)


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = (
        "livro",
        "leitor",
        "data_emprestimo",
        "data_prevista",
        "status",
    )
    list_filter = ("status",)
