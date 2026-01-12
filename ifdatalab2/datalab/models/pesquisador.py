from django.db import models
from django.contrib.auth.models import User
from .campus import Campus
from .grupo_pesquisa import GrupoPesquisa

class Pesquisador(models.Model):
    class Funcao(models.TextChoices):
        PROFESSOR = 'Professor', 'Professor'
        TECNICO = 'Técnico', 'Técnico'
        ALUNO = 'Aluno', 'Aluno'
        ALUMNI = 'Alumni', 'Alumni'

    nome_completo = models.CharField(max_length=255)
    idlattes = models.CharField(max_length=100, unique=True)
    funcao = models.CharField(max_length=50, choices=Funcao.choices)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True)
    usuario_vinculado = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ultima_extracao_em = models.DateTimeField(null=True, blank=True)
    status_extracao = models.CharField(max_length=50, default='Pendente')
    grupo = models.ForeignKey(GrupoPesquisa, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome_completo
