from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

def lista_publica_grupos(request):
    grupos = GrupoPesquisa.objects.annotate(
        total_membros=Count('pesquisador', distinct=True),
        total_publicacoes=Count('pesquisador__publicacoes', distinct=True),
        total_projetos=Count('pesquisador__projetos', distinct=True)
    )
    
    context = {
        'grupos': grupos
    }
    return render(request, 'datalab/public/lista_grupos_pesquisa.html', context)
