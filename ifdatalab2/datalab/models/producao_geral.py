from django.db import models
from .pesquisador import Pesquisador
from .campus import Campus

class ProducaoGeral(models.Model):
    pesquisador = models.OneToOneField(Pesquisador, on_delete=models.CASCADE, primary_key=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    ultima_atualizacao = models.DateTimeField(null=True, blank=True)
    producoes_tecnicas = models.IntegerField(default=0)
    producoes_bibliograficas = models.IntegerField(default=0)
    orientacoes = models.IntegerField(default=0)
    projetos_pesquisa = models.IntegerField(default=0)

    def __str__(self):
        return f"Produções de {self.pesquisador.nome_completo}"
    class Meta:
        verbose_name = "Produção Geral"
        verbose_name_plural = "Produções Gerais"