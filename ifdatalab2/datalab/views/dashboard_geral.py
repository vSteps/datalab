from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

def dashboard_geral(request):
    metrics = {
        'total_autores': Pesquisador.objects.count(),
        'total_publicacoes': Publicacao.objects.count(),
        'total_orientacoes': Orientacao.objects.count(),
        'total_producoes': ProducaoGeral.objects.aggregate(total=Sum('producoes_tecnicas'))['total'] or 0,
    }

    context = {
        'metrics': metrics,
        'grupos': GrupoPesquisa.objects.all(),
    }
    return render(request, 'dashboard/painel.html', context)
