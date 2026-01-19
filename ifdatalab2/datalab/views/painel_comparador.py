from django.shortcuts import render
from datalab.models import (
    Pesquisador,
    PesquisadoresCCSL,
    PesquisadoresDGP,
    RedmineCCSL,
    RedmineDGP,
    CCSLNaoDGP,
    RedmineNaoDGP,
)
from datalab.permissions import is_admin_global
from datalab.decorators import admin_grupo_ou_global


@admin_grupo_ou_global
def painel_comparador(request):

    # =========================
    # ADMIN GLOBAL
    # =========================
    if is_admin_global(request.user):

        ccsl = PesquisadoresCCSL.objects.filter(
            nome_ccsl__isnull=False
        ).exclude(nome_ccsl="")

        dgp = PesquisadoresDGP.objects.filter(
            nome_dgp__isnull=False
        ).exclude(nome_dgp="")

        ccsl_nao_dgp = CCSLNaoDGP.objects.filter(
            nome__isnull=False
        ).exclude(nome="")

        # 🚨 REDMINE NÃO DEPENDE DE PESQUISADOR
        redmine_nao_dgp = RedmineNaoDGP.objects.filter(
            nome__isnull=False
        ).exclude(nome="")

        total_redmine = (
            RedmineCCSL.objects.filter(nome__isnull=False).exclude(nome="").count()
            +
            RedmineDGP.objects.filter(nome__isnull=False).exclude(nome="").count()
        )

    # =========================
    # ADMIN DE GRUPO
    # =========================
    else:
        grupo = request.user.admingrupo.grupo

        # Apenas para CCSL / DGP
        nomes_pesquisadores = Pesquisador.objects.filter(
            grupo=grupo,
            nome_completo__isnull=False
        ).exclude(
            nome_completo=""
        ).values_list("nome_completo", flat=True)

        ccsl = PesquisadoresCCSL.objects.filter(
            nome_ccsl__in=nomes_pesquisadores
        )

        dgp = PesquisadoresDGP.objects.filter(
            nome_dgp__in=nomes_pesquisadores
        )

        ccsl_nao_dgp = CCSLNaoDGP.objects.filter(
            nome__in=nomes_pesquisadores
        )

        # 🚨 REDMINE CONTINUA INTEIRO (só limpa None/vazio)
        redmine_nao_dgp = RedmineNaoDGP.objects.filter(
            nome__isnull=False
        ).exclude(nome="")

        total_redmine = (
            RedmineCCSL.objects.filter(nome__isnull=False).exclude(nome="").count()
            +
            RedmineDGP.objects.filter(nome__isnull=False).exclude(nome="").count()
        )

    context = {
        "ccsl": ccsl,
        "dgp": dgp,
        "ccsl_nao_dgp": ccsl_nao_dgp,
        "redmine_nao_dgp": redmine_nao_dgp,
        "total_ccsl": ccsl.count(),
        "total_dgp": dgp.count(),
        "total_redmine": total_redmine,
    }

    return render(request, "dashboard/painel_comparador.html", context)
