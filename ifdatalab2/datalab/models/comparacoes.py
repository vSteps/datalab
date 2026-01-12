from django.db import models

class CCSLNaoDGP(models.Model):
    nome = models.CharField(max_length=256)

    class Meta:
        db_table = "ccsl_nao_dgp"


class RedmineNaoDGP(models.Model):
    nome = models.CharField(max_length=256)

    class Meta:
        db_table = "redmine_nao_dgp"
