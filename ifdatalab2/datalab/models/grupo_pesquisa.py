from django.db import models
from django.contrib.auth.models import User

class GrupoPesquisa(models.Model):
    nome = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    ano_formacao = models.IntegerField(blank=True, null=True)
    link_cnpq = models.URLField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    usuarios = models.ManyToManyField(User, related_name='grupos_pesquisa')

    def __str__(self):
        return self.nome
