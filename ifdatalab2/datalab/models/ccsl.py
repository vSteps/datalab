from django.db import models

class PesquisadoresCCSL(models.Model):
    nome_ccsl = models.CharField(max_length=256)
    tipo = models.CharField(max_length=100, default='desconhecido')

    class Meta:
        db_table = "pesquisadores_site"
