from django.db import models

class Campus(models.Model):
    nome_campus = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome_campus

    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campi"