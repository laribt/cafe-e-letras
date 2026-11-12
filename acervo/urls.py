
from django.urls import path

from . import views


urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("livros/", views.lista_livros, name="lista_livros"),
    path(
        "livros/novo/",
        views.cadastrar_livro,
        name="cadastrar_livro"
    ),
    path(
        "leitores/",
        views.lista_leitores,
        name="lista_leitores"
    ),
    path(
        "leitores/novo/",
        views.cadastrar_leitor,
        name="cadastrar_leitor"
    ),
    path(
        "emprestimos/",
        views.lista_emprestimos,
        name="lista_emprestimos"
    ),
    path(
        "emprestimos/novo/",
        views.novo_emprestimo,
        name="novo_emprestimo"
    ),
    path(
        "emprestimos/<int:emprestimo_id>/devolver/",
        views.devolver_livro,
        name="devolver_livro"
    ),
]
