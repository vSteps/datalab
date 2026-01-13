from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
import json
from scholarly import scholarly
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)



def get_scholar_info(pesquisador):
    try:
        search_query = scholarly.search_author(pesquisador.nome_completo)
        author = next(search_query, None)
        if author:
            author = scholarly.fill(author)
            return {
                'citações_totais': author.get('citedby', 0),
                'índice_h': author.get('hindex', 0),
                'índice_i10': author.get('i10index', 0),
            }
    except Exception as e:
        print(f"Erro ao obter dados do Google Scholar para {pesquisador.nome_completo}: {e}")
    
    return {
        'citações_totais': 0,
        'índice_h': 0,
        'índice_i10': 0,
    }

def detalhes_pesquisador_publico(request, pesquisador_id):
    """
    Exibe o perfil completo de um pesquisador com métricas e gráficos.
    """
    pesquisador = get_object_or_404(Pesquisador, id=pesquisador_id)
    
    # Consultas de produção
    publicacoes = pesquisador.publicacoes.all().select_related('campus').order_by('-id')
    projetos = pesquisador.projetos.all().select_related('campus')
    orientacoes = pesquisador.orientacoes.all().select_related('campus').order_by('-ano')
    
    # Métricas
    metrics = {
        'total_pubs': publicacoes.count(),
        'total_projs': projetos.count(),
        'total_oris': orientacoes.count(),
    }
    
    # Gráfico de evolução (Orientações)
    prod_por_ano = orientacoes.filter(ano__isnull=False).values('ano').annotate(count=Count('id')).order_by('ano')
    
    dados_grafico = {
        'labels': json.dumps([str(p['ano']) for p in prod_por_ano]),
        'data': json.dumps([p['count'] for p in prod_por_ano]),
    }

    context = {
        'pesquisador': pesquisador,
        'publicacoes': publicacoes,
        'projetos': projetos,
        'orientacoes': orientacoes,
        'metrics': metrics,
        'dados_grafico': dados_grafico,
        'scholar_info': get_scholar_info(pesquisador),
    }
    
    return render(request, 'datalab/public/detalhes_pesquisador.html', context)