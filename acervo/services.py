
from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from .models import Emprestimo, Livro


@transaction.atomic
def registrar_emprestimo(livro, leitor, data_prevista):
    if data_prevista < date.today():
        raise ValidationError(
            "A data prevista não pode estar no passado."
        )

    atualizado = Livro.objects.filter(
        pk=livro.pk,
        quantidade_disponivel__gt=0
    ).update(
        quantidade_disponivel=F("quantidade_disponivel") - 1
    )

    if atualizado == 0:
        raise ValidationError(
            "Este livro não possui exemplares disponíveis."
        )

    emprestimo = Emprestimo.objects.create(
        livro=livro,
        leitor=leitor,
        data_prevista=data_prevista,
        status="aberto"
    )

    return emprestimo


@transaction.atomic
def registrar_devolucao(emprestimo):
    atualizado = Emprestimo.objects.filter(
        pk=emprestimo.pk,
        status="aberto"
    ).update(
        status="devolvido",
        data_devolucao=date.today()
    )

    if atualizado == 0:
        raise ValidationError(
            "Este empréstimo já foi devolvido."
        )

    Livro.objects.filter(
        pk=emprestimo.livro_id
    ).update(
        quantidade_disponivel=F("quantidade_disponivel") + 1
    )
