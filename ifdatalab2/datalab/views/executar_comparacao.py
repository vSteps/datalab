from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages

@staff_member_required
def executar_comparacao(request):
    if request.method == "POST":
        try:
            response = requests.post(
                "http://10.26.1.73:5678/webhook/comparar",
                json={"origem": "datalab"},
                timeout=120
            )
            response.raise_for_status()
            messages.success(request, "Comparação executada com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao executar comparação: {e}")

        return redirect("datalab:painel_comparador")

    return redirect("datalab:painel_comparador")