from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
import re
import json
from collections import Counter
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

def dashboard_grupo(request, grupo_id):
    grupo = get_object_or_404(GrupoPesquisa, id=grupo_id)
    
    view_selecionada = request.GET.get('view', 'pesquisadores')

    # 1. Métricas Gerais
    metrics = {
        'total_autores': Pesquisador.objects.filter(grupo=grupo).count(),
        'total_publicacoes': Publicacao.objects.filter(pesquisador__grupo=grupo).count(),
        'total_orientacoes': Orientacao.objects.filter(pesquisador__grupo=grupo).count(),
        'total_producoes': ProducaoGeral.objects.filter(pesquisador__grupo=grupo).aggregate(
            total=Sum('producoes_tecnicas')
        )['total'] or 0,
    }

    # 2. Dados para a Tabela de Membros (Resumo) - ESSA PARTE FALTAVA
    membros_tabela = Pesquisador.objects.filter(grupo=grupo).annotate(
        qtd_publicacoes=Count('publicacoes', distinct=True),
        qtd_orientacoes=Count('orientacoes', distinct=True),
    ).order_by('-qtd_publicacoes')

    # 3. Lógica dos Gráficos (Ano e Pizza)
    def extrair_anos_de_titulos(lista_titulos):
        anos_encontrados = []
        for titulo in lista_titulos:
            if titulo:
                match = re.search(r'\b(20\d{2}|19\d{2})\b', titulo)
                if match:
                    anos_encontrados.append(match.group(0))
        return Counter(anos_encontrados)

    qs_pubs = Publicacao.objects.filter(pesquisador__grupo=grupo).values_list('titulo', flat=True)
    qs_oris = Orientacao.objects.filter(pesquisador__grupo=grupo).values_list('titulo', flat=True)

    counter_pubs = extrair_anos_de_titulos(qs_pubs)
    counter_oris = extrair_anos_de_titulos(qs_oris)
    todos_anos = sorted(list(set(list(counter_pubs.keys()) + list(counter_oris.keys()))))

    data_pubs = [counter_pubs.get(ano, 0) for ano in todos_anos]
    data_oris = [counter_oris.get(ano, 0) for ano in todos_anos]
    
    total_biblio = metrics['total_publicacoes']
    total_tec = metrics['total_producoes']

    lista_detalhada = []
    if view_selecionada == 'publicacoes':
        lista_detalhada = Publicacao.objects.filter(pesquisador__grupo=grupo).select_related('pesquisador', 'campus').order_by('-id')
    elif view_selecionada == 'orientacoes':
        lista_detalhada = Orientacao.objects.filter(pesquisador__grupo=grupo).select_related('pesquisador', 'campus').order_by('-ano')
    elif view_selecionada == 'producoes':
        lista_detalhada = ProducaoGeral.objects.filter(pesquisador__grupo=grupo).select_related('pesquisador', 'campus')

    # 4. Contexto Base
    context = {
        'grupo': grupo,
        'metrics': metrics,
        'view_selecionada': view_selecionada,
        'membros_tabela': membros_tabela, # Enviando os dados calculados para a tabela fixa
        'lista_detalhada': lista_detalhada,
        
        # Gráficos
        'chart_anos_labels': json.dumps(todos_anos),
        'chart_data_pubs': json.dumps(data_pubs),
        'chart_data_oris': json.dumps(data_oris),
        'chart_pizza_data': json.dumps([total_biblio, total_tec]),
    }


    return render(request, 'datalab/dashboard_grupo.html', context)