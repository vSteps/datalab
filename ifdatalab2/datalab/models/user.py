from django.conf import settings
from django.db import models
from datalab.models.grupo_pesquisa import GrupoPesquisa

class AdminGrupo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    grupo = models.ForeignKey(
        GrupoPesquisa,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} → {self.grupo.nome}"