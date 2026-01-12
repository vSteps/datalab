from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
import json
from django.contrib.auth import logout
from django.shortcuts import redirect
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

def detalhes_grupo_publico(request, grupo_id):

    grupo = get_object_or_404(GrupoPesquisa, id=grupo_id)
    
    metrics = {
        'total_autores': Pesquisador.objects.filter(grupo=grupo).count(),
        'total_publicacoes': Publicacao.objects.filter(pesquisador__grupo=grupo).count(),
        'total_orientacoes': Orientacao.objects.filter(pesquisador__grupo=grupo).count(),
        'total_projetos': ProjetoPesquisa.objects.filter(pesquisador__grupo=grupo).count(),
    }
    
    orientacoes_por_ano = Orientacao.objects.filter(pesquisador__grupo=grupo, ano__isnull=False) \
                                       .values('ano') \
                                       .annotate(count=Count('id')) \
                                       .order_by('ano')
    
    dados_grafico = {
        'labels': json.dumps([str(item['ano']) for item in orientacoes_por_ano]),
        'data': json.dumps([item['count'] for item in orientacoes_por_ano]),
    }


    context = {
        'grupo': grupo,
        'pesquisadores': Pesquisador.objects.filter(grupo=grupo).select_related('campus'),
        'metrics': metrics,
        'dados_grafico': dados_grafico,
    }
    return render(request, 'datalab/public/detalhes_grupo.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')