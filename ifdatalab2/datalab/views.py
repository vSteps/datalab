from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Pesquisador, Publicacao, Orientacao, ProducaoGeral

def dashboard_geral(request):
    metrics = {
        'total_autores': Pesquisador.objects.count(),
        'total_publicacoes': Publicacao.objects.count(),
        'total_orientacoes': Orientacao.objects.count(),
        'total_producoes': ProducaoGeral.objects.aggregate(total=Sum('producoes_tecnicas'))['total'] or 0,
    }

    # Lógica de visualização
    view_selecionada = request.GET.get('view', 'pesquisadores')
    
    context = {
        'metrics': metrics,
        'view_selecionada': view_selecionada,
    }

    if view_selecionada == 'pesquisadores':
        context['pesquisadores_lattes'] = Pesquisador.objects.select_related('campus').all()
    elif view_selecionada == 'publicacoes':
        context['publicacoes'] = Publicacao.objects.select_related('pesquisador', 'campus').all()

    return render(request, 'ifdatalab/geral.html', context)