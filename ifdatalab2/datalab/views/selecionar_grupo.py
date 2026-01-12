from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum 
from datalab.models import (
    Pesquisador, GrupoPesquisa, Publicacao, Orientacao, ProducaoGeral
)

@login_required
def selecionar_grupo(request):
    grupos_usuario = request.user.grupos_pesquisa.all() 
    if grupos_usuario.count() == 1:
        return redirect('datalab:dashboard_grupo', grupo_id=grupos_usuario.first().id)

    return render(request, 'datalab/selecionar_grupo.html', {'grupos': grupos_usuario})

