
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Livro, Leitor, Emprestimo
from .services import registrar_emprestimo, registrar_devolucao


class EmprestimoTests(TestCase):

    def setUp(self):
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            genero="Romance",
            quantidade_total=2,
            quantidade_disponivel=2
        )

        self.leitor = Leitor.objects.create(
            nome="Ana Souza"
        )

        self.data_prevista = date.today() + timedelta(days=7)

    def test_emprestimo_reduz_disponibilidade(self):
        emprestimo = registrar_emprestimo(
            self.livro,
            self.leitor,
            self.data_prevista
        )

        self.livro.refresh_from_db()

        self.assertEqual(
            self.livro.quantidade_disponivel,
            1
        )
        self.assertEqual(emprestimo.status, "aberto")

    def test_nao_permite_emprestimo_sem_estoque(self):
        self.livro.quantidade_disponivel = 0
        self.livro.save()

        with self.assertRaises(ValidationError):
            registrar_emprestimo(
                self.livro,
                self.leitor,
                self.data_prevista
            )

        self.assertEqual(Emprestimo.objects.count(), 0)

    def test_devolucao_restaura_disponibilidade(self):
        emprestimo = registrar_emprestimo(
            self.livro,
            self.leitor,
            self.data_prevista
        )

        registrar_devolucao(emprestimo)

        self.livro.refresh_from_db()
        emprestimo.refresh_from_db()

        self.assertEqual(
            self.livro.quantidade_disponivel,
            2
        )
        self.assertEqual(emprestimo.status, "devolvido")

    def test_nao_permite_devolucao_duplicada(self):
        emprestimo = registrar_emprestimo(
            self.livro,
            self.leitor,
            self.data_prevista
        )

        registrar_devolucao(emprestimo)

        with self.assertRaises(ValidationError):
            registrar_devolucao(emprestimo)

        self.livro.refresh_from_db()

        self.assertEqual(
            self.livro.quantidade_disponivel,
            2
        )
