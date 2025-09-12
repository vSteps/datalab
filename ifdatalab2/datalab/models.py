from django.db import models
from django.contrib.auth.models import User

class Campus(models.Model):
    nome_campus = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome_campus
    
    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campi"

class GrupoPesquisa(models.Model):
    nome = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    criado_por = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    usuarios = models.ManyToManyField('auth.User', related_name='grupos_pesquisa')

    def __str__(self):
        return self.nome
    
class Pesquisador(models.Model):
    class Funcao(models.TextChoices):
        PROFESSOR = 'Professor', 'Professor'
        TECNICO = 'Técnico', 'Técnico'
        ALUNO = 'Aluno', 'Aluno'
        ALUMNI = 'Alumni', 'Alumni'

    nome_completo = models.CharField(max_length=255)
    idlattes = models.CharField(max_length=100, unique=True)
    funcao = models.CharField(max_length=50, choices=Funcao.choices, default=Funcao.ALUNO)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True, help_text="Campus principal do pesquisador.")
    usuario_vinculado = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Conta de login associada a este perfil.")
    created_at = models.DateTimeField(auto_now_add=True)
    ultima_extracao_em = models.DateTimeField(null=True, blank=True, help_text="Data e hora da última extração de dados do Lattes.")
    status_extracao = models.CharField(max_length=50, default='Pendente')
    grupo = models.ForeignKey(GrupoPesquisa, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.nome_completo
    class Meta:
        verbose_name = "Pesquisador"
        verbose_name_plural = "Pesquisadores"


class Publicacao(models.Model):
    pesquisador = models.ForeignKey(Pesquisador, on_delete=models.CASCADE, related_name='publicacoes')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    titulo = models.TextField()
    categoria = models.TextField(blank=True, null=True)
    subcategoria = models.TextField(blank=True, null=True)
    ccsl = models.BooleanField(default=False, help_text="Indica se a publicação está relacionada ao CCSL.")

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"

class Orientacao(models.Model):
    pesquisador = models.ForeignKey(Pesquisador, on_delete=models.CASCADE, related_name='orientacoes')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    titulo = models.TextField()
    ano = models.IntegerField(null=True, blank=True)
    discentes = models.TextField(blank=True, null=True, help_text="Nomes dos alunos orientados.")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Orientação"
        verbose_name_plural = "Orientações"

class ProjetoPesquisa(models.Model):
    pesquisador = models.ForeignKey(Pesquisador, on_delete=models.CASCADE, related_name='projetos')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    titulo = models.TextField()
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Projeto de Pesquisa"
        verbose_name_plural = "Projetos de Pesquisa"

class ProducaoGeral(models.Model):
    pesquisador = models.OneToOneField(Pesquisador, on_delete=models.CASCADE, primary_key=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    ultima_atualizacao = models.DateTimeField(null=True, blank=True)
    producoes_tecnicas = models.IntegerField(default=0)
    producoes_bibliograficas = models.IntegerField(default=0)
    orientacoes = models.IntegerField(default=0)
    projetos_pesquisa = models.IntegerField(default=0)

    def __str__(self):
        return f"Produções de {self.pesquisador.nome_completo}"
    class Meta:
        verbose_name = "Produção Geral"
        verbose_name_plural = "Produções Gerais"
