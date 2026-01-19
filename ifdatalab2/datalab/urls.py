from django.urls import path, include
from datalab.views import *

app_name = 'datalab'

urlpatterns = [
    path("", home_publica, name='home_publica'),

    path("pesquisadores/", lista_publica_pesquisadores, name='lista_publica_pesquisadores'),
    path("grupos/", lista_publica_grupos, name='lista_publica_grupos'),
    path("grupos/<int:grupo_id>/", detalhes_grupo_publico, name='detalhes_grupo_publico'),
    path("pesquisadores/<int:pesquisador_id>/", detalhes_pesquisador_publico, name='detalhes_pesquisador_publico'),

    path("painel/", dashboard_geral, name='dashboard_geral'),
    path("painel/grupo/<int:grupo_id>/", dashboard_grupo, name='dashboard_grupo'),
    path("painel/selecionar-grupo/", selecionar_grupo, name="selecionar_grupo"),

    path("painel/comparador/", painel_comparador, name="painel_comparador"),
    path("painel/comparador/executar/", executar_comparacao, name="executar_comparacao"),

    path("extracao/", include("extracao.urls")),

    path("logout/", logout_view, name='logout'),
]
