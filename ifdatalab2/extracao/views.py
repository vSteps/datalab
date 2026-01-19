from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from datalab.models import GrupoPesquisa, Pesquisador
from datalab.permissions import is_admin_global
from datalab.decorators import admin_grupo_ou_global

from extracao.models import Extracao
from extracao.services.runner import disparar_extracao


@admin_grupo_ou_global
def painel_extracao(request):

    if is_admin_global(request.user):
        grupos = GrupoPesquisa.objects.all()
    else:
        grupos = GrupoPesquisa.objects.filter(
            id=request.user.admingrupo.grupo.id
        )

    grupos_com_pesquisadores = []
    for grupo in grupos:
        pesquisadores = Pesquisador.objects.filter(grupo=grupo)
        grupos_com_pesquisadores.append({
            "grupo": grupo,
            "pesquisadores": pesquisadores
        })

    return render(
        request,
        "dashboard/painel_extracao.html",
        {"grupos": grupos_com_pesquisadores}
    )


@admin_grupo_ou_global
def executar_extracao(request, pesquisador_id):

    if is_admin_global(request.user):
        pesquisador = get_object_or_404(Pesquisador, id=pesquisador_id)
    else:
        grupo = request.user.admingrupo.grupo
        pesquisador = get_object_or_404(
            Pesquisador,
            id=pesquisador_id,
            grupo=grupo
        )

    extracao = Extracao.objects.create(
        pesquisador=pesquisador,
        status="PENDENTE"
    )

    disparar_extracao(extracao)

    messages.success(
        request,
        f"Extração iniciada para {pesquisador.nome_completo}"
    )

    return redirect(
        "extracao:status_extracao",
        extracao_id=extracao.id
    )

@admin_grupo_ou_global
def status_extracao(request, extracao_id):

    if is_admin_global(request.user):
        extracao = get_object_or_404(Extracao, id=extracao_id)
    else:
        grupo = request.user.admingrupo.grupo
        extracao = get_object_or_404(
            Extracao,
            id=extracao_id,
            pesquisador__grupo=grupo
        )

    return render(
        request,
        "extracao/status.html",
        {"extracao": extracao}
    )