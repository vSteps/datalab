from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Pesquisador, Publicacao, Orientacao, ProducaoGeral, GrupoPesquisa


@login_required
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
    return render(request, 'datalab/dashboard_geral.html', context)


@login_required
def selecionar_grupo(request):
    grupos_usuario = request.user.grupos_pesquisa.all() 
    if grupos_usuario.count() == 1:
        return redirect('dashboard_grupo', grupo_id=grupos_usuario.first().id)

    return render(request, 'datalab/selecionar_grupo.html', {'grupos': grupos_usuario})


@login_required
def dashboard_grupo(request, grupo_id):
    grupo = get_object_or_404(GrupoPesquisa, id=grupo_id)

    view_selecionada = request.GET.get('view', 'pesquisadores')

    metrics = {
        'total_autores': Pesquisador.objects.filter(grupo=grupo).count(),
        'total_publicacoes': Publicacao.objects.filter(pesquisador__grupo=grupo).count(),
        'total_orientacoes': Orientacao.objects.filter(pesquisador__grupo=grupo).count(),
        'total_producoes': ProducaoGeral.objects.filter(pesquisador__grupo=grupo).aggregate(
            total=Sum('producoes_tecnicas')
        )['total'] or 0,
    }

    context = {
        'grupo': grupo,
        'metrics': metrics,
        'view_selecionada': view_selecionada,
    }

    if view_selecionada == 'pesquisadores':
        context['pesquisadores'] = Pesquisador.objects.filter(grupo=grupo).select_related('campus')
    elif view_selecionada == 'publicacoes':
        context['publicacoes'] = Publicacao.objects.filter(pesquisador__grupo=grupo).select_related('pesquisador', 'campus')
    elif view_selecionada == 'orientacoes':
        context['orientacoes'] = Orientacao.objects.filter(pesquisador__grupo=grupo).select_related('pesquisador', 'campus')
    elif view_selecionada == 'producoes':
        context['producoes'] = ProducaoGeral.objects.filter(pesquisador__grupo=grupo).select_related('pesquisador', 'campus')

    return render(request, 'datalab/dashboard_grupo.html', context)


@login_required
def home_redirect(request):
    grupo_id = request.session.get("grupo_id")
    if grupo_id:
        return redirect("dashboard_grupo", grupo_id=grupo_id)
    else:
        return redirect("selecionar_grupo")