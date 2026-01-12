from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

from datalab.models import (
    PesquisadoresCCSL,
    PesquisadoresDGP,
    RedmineCCSL,
    RedmineDGP,
    CCSLNaoDGP,
    RedmineNaoDGP,
)

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

@staff_member_required
def painel_comparador(request):
    context = {
        "ccsl": PesquisadoresCCSL.objects.exclude(nome_ccsl__isnull=True).exclude(nome_ccsl=""),
        "dgp": PesquisadoresDGP.objects.exclude(nome_dgp__isnull=True).exclude(nome_dgp=""),
        "ccsl_nao_dgp": CCSLNaoDGP.objects.exclude(nome__isnull=True).exclude(nome=""),
        "redmine_nao_dgp": RedmineNaoDGP.objects.exclude(nome__isnull=True).exclude(nome=""),
        "total_ccsl": PesquisadoresCCSL.objects.count(),
        "total_dgp": PesquisadoresDGP.objects.count(),
        "total_redmine": RedmineCCSL.objects.count() + RedmineDGP.objects.count(),
    }
    return render(request, "dashboard/painel_comparador.html", context)