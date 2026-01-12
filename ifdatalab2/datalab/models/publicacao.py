from django.db import models
from .pesquisador import Pesquisador
from .campus import Campus

class Publicacao(models.Model):
    pesquisador = models.ForeignKey(Pesquisador, on_delete=models.CASCADE, related_name='publicacoes')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    titulo = models.TextField()
    categoria = models.TextField(blank=True, null=True)
    subcategoria = models.TextField(blank=True, null=True)
    ccsl = models.BooleanField(default=False)
