from django.db import models
from .pesquisador import Pesquisador
from .campus import Campus

class ProjetoPesquisa(models.Model):
    pesquisador = models.ForeignKey(Pesquisador, on_delete=models.CASCADE, related_name='projetos')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    titulo = models.TextField()
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Projeto de Pesquisa"
        verbose_name_plural = "Projetos de Pesquisa"
