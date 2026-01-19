from django.contrib import admin
from .models import Campus, Pesquisador, Publicacao, Orientacao, ProducaoGeral, GrupoPesquisa
from .models import AdminGrupo

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('nome_campus',)
    search_fields = ('nome_campus',)

@admin.register(Pesquisador)
class PesquisadorAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'idlattes', 'campus', 'funcao', 'usuario_vinculado')
    list_filter = ('campus', 'funcao')
    search_fields = ('nome_completo', 'idlattes')
    autocomplete_fields = ('usuario_vinculado',) # Facilita a vinculação
    

admin.site.register(Publicacao)
admin.site.register(Orientacao)
admin.site.register(ProducaoGeral)
admin.site.register(GrupoPesquisa)
admin.site.register(AdminGrupo)