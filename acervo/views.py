
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .forms import LivroForm, LeitorForm, EmprestimoForm
from .models import Livro, Leitor, Emprestimo
from .services import registrar_emprestimo, registrar_devolucao


@login_required
def inicio(request):
    return render(request, "acervo/inicio.html")


@login_required
def lista_livros(request):
    busca = request.GET.get("busca", "").strip()

    livros = Livro.objects.all().order_by("titulo")

    if busca:
        livros = livros.filter(
            Q(titulo__icontains=busca) |
            Q(autor__icontains=busca)
        )

    return render(
        request,
        "acervo/livros.html",
        {"livros": livros, "busca": busca}
    )


@login_required
def cadastrar_livro(request):
    form = LivroForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Livro cadastrado com sucesso.")
        return redirect("lista_livros")

    return render(
        request,
        "acervo/formulario.html",
        {"form": form, "titulo": "Cadastrar livro"}
    )


@login_required
def cadastrar_leitor(request):
    form = LeitorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Leitor cadastrado com sucesso.")
        return redirect("lista_leitores")

    return render(
        request,
        "acervo/formulario.html",
        {"form": form, "titulo": "Cadastrar leitor"}
    )


@login_required
def lista_leitores(request):
    leitores = Leitor.objects.all().order_by("nome")

    return render(
        request,
        "acervo/leitores.html",
        {"leitores": leitores}
    )


@login_required
def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.select_related(
        "livro", "leitor"
    ).order_by("-id")

    return render(
        request,
        "acervo/emprestimos.html",
        {"emprestimos": emprestimos}
    )


@login_required
def novo_emprestimo(request):
    form = EmprestimoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            emprestimo = registrar_emprestimo(
                form.cleaned_data["livro"],
                form.cleaned_data["leitor"],
                form.cleaned_data["data_prevista"]
            )
        except ValidationError as erro:
            form.add_error(None, erro)
        else:
            messages.success(
                request,
                f"Empréstimo {emprestimo.pk} registrado com sucesso."
            )
            return redirect("lista_emprestimos")

    return render(
        request,
        "acervo/formulario.html",
        {"form": form, "titulo": "Novo empréstimo"}
    )


@login_required
def devolver_livro(request, emprestimo_id):
    if request.method != "POST":
        return redirect("lista_emprestimos")

    emprestimo = get_object_or_404(
        Emprestimo,
        pk=emprestimo_id
    )

    try:
        registrar_devolucao(emprestimo)
    except ValidationError as erro:
        messages.error(request, "; ".join(erro.messages))
    else:
        messages.success(
            request,
            "Devolução registrada com sucesso."
        )

    return redirect("lista_emprestimos")
