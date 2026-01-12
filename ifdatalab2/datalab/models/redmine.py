from django.db import models

class RedmineCCSL(models.Model):
    nome = models.CharField(max_length=256)

    class Meta:
        db_table = "redmine_ccsl"


class RedmineDGP(models.Model):
    nome = models.CharField(max_length=256)

    class Meta:
      db_table = "redmine_dgp"