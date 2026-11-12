
from django.db import models
from django.core.validators import MinValueValidator


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    genero = models.CharField(max_length=100)
    quantidade_total = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    quantidade_disponivel = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class Leitor(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Leitor"
        verbose_name_plural = "Leitores"

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ("aberto", "Em aberto"),
        ("devolvido", "Devolvido"),
    ]

    livro = models.ForeignKey(
        Livro,
        on_delete=models.PROTECT
    )
    leitor = models.ForeignKey(
        Leitor,
        on_delete=models.PROTECT
    )
    data_emprestimo = models.DateField(auto_now_add=True)
    data_prevista = models.DateField()
    data_devolucao = models.DateField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="aberto"
    )

    def __str__(self):
        return f"{self.livro.titulo} - {self.leitor.nome}"
