from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

def lista_publica_pesquisadores(request):
    pesquisadores = Pesquisador.objects.all().select_related('campus', 'grupo').annotate(
        total_pubs=Count('publicacoes', distinct=True),
        total_projs=Count('projetos', distinct=True),
        total_oris=Count('orientacoes', distinct=True)
    ).order_by('nome_completo')
    
    context = {
        'pesquisadores': pesquisadores
    }
    return render(request, 'datalab/public/lista_pesquisadores.html', context)
