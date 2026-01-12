from django.db import models
from .pesquisador import Pesquisador  
from .campus import Campus

class Orientacao(models.Model):
    pesquisador = models.ForeignKey(Pesquisador, on_delete=models.CASCADE, related_name='orientacoes')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    titulo = models.TextField()
    ano = models.IntegerField(null=True, blank=True)
    discentes = models.TextField(blank=True, null=True, help_text="Nomes dos alunos orientados.")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Orientação"
        verbose_name_plural = "Orientações"