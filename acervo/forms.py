
from datetime import date

from django import forms

from .models import Livro, Leitor


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            "titulo",
            "autor",
            "genero",
            "quantidade_total",
        ]

    def save(self, commit=True):
        livro = super().save(commit=False)

        if livro.pk is None:
            livro.quantidade_disponivel = livro.quantidade_total

        if commit:
            livro.save()
            self.save_m2m()

        return livro


class LeitorForm(forms.ModelForm):
    class Meta:
        model = Leitor
        fields = ["nome", "telefone", "email"]


class EmprestimoForm(forms.Form):
    livro = forms.ModelChoiceField(
        queryset=Livro.objects.none(),
        label="Livro"
    )

    leitor = forms.ModelChoiceField(
        queryset=Leitor.objects.all(),
        label="Leitor"
    )

    data_prevista = forms.DateField(
        label="Data prevista de devolução",
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["livro"].queryset = Livro.objects.filter(
            quantidade_disponivel__gt=0
        ).order_by("titulo")

    def clean_data_prevista(self):
        data_prevista = self.cleaned_data["data_prevista"]

        if data_prevista < date.today():
            raise forms.ValidationError(
                "A data prevista não pode estar no passado."
            )

        return data_prevista
