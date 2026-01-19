from django.db import models
from datalab.models import Pesquisador

class Extracao(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("RODANDO", "Rodando"),
        ("SUCESSO", "Sucesso"),
        ("ERRO", "Erro"),
    ]

    pesquisador = models.ForeignKey(Pesquisador, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    erro = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pesquisador.nome_completo} - {self.status}"