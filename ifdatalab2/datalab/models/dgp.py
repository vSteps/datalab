from django.db import models

class PesquisadoresDGP(models.Model):
    nome_dgp = models.CharField(max_length=256)

    class Meta:
        db_table = "pesquisadores_dgp"
