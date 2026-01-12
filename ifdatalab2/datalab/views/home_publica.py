from django.shortcuts import render
from django.db.models import Count, Sum
import re
import json
from collections import Counter
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

def home_publica(request):
    # 1. MÉTRICAS GERAIS (Cards do topo)
    metrics = {
        'total_pesquisadores': Pesquisador.objects.count(),
        'total_grupos': GrupoPesquisa.objects.count(),
        'total_publicacoes': Publicacao.objects.count(),
        'total_orientacoes': Orientacao.objects.count(),
        'total_producoes': ProducaoGeral.objects.aggregate(total=Sum('producoes_tecnicas'))['total'] or 0,
    }

    def extrair_anos_de_titulos(lista_titulos):
        anos_encontrados = []
        for titulo in lista_titulos:
            if titulo:
                match = re.search(r'\b(20\d{2}|19\d{2})\b', titulo)
                if match:
                    anos_encontrados.append(match.group(0))
        return Counter(anos_encontrados)

    titulos_publicacoes = Publicacao.objects.values_list('titulo', flat=True)
    titulos_orientacoes = Orientacao.objects.values_list('titulo', flat=True)

    counter_pubs = extrair_anos_de_titulos(titulos_publicacoes)
    counter_oris = extrair_anos_de_titulos(titulos_orientacoes)

    todos_anos = sorted(list(set(list(counter_pubs.keys()) + list(counter_oris.keys()))))

    data_pubs = [counter_pubs.get(ano, 0) for ano in todos_anos]
    data_oris = [counter_oris.get(ano, 0) for ano in todos_anos]

    # 3. GRÁFICO 2 Top 5 Grupos por Publicações
    top_grupos_query = Publicacao.objects.filter(pesquisador__grupo__isnull=False) \
        .values('pesquisador__grupo__nome') \
        .annotate(total=Count('id')) \
        .order_by('-total')[:5]
    
    grupos_labels = [item['pesquisador__grupo__nome'] for item in top_grupos_query]
    grupos_data = [item['total'] for item in top_grupos_query]

    # 4. GRÁFICO 3: Pizza (Distribuição)
    total_biblio = metrics['total_publicacoes']
    total_tec = metrics['total_producoes']

    context = {
        'metrics': metrics,
        'chart_anos_labels': json.dumps(todos_anos),
        'chart_data_pubs': json.dumps(data_pubs),
        'chart_data_oris': json.dumps(data_oris),
        'chart_grupos_labels': json.dumps(grupos_labels),
        'chart_grupos_data': json.dumps(grupos_data),
        'chart_pizza_data': json.dumps([total_biblio, total_tec]),
    }
    
    return render(request, 'datalab/public/home.html', context)