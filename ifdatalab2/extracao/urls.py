from django.urls import path
from . import views

app_name = "extracao"

urlpatterns = [
    path("", views.painel_extracao, name="painel_extracao"),
    path("executar/<int:pesquisador_id>/", views.executar_extracao, name="executar_extracao"),
    path(
        "status/<int:extracao_id>/",
        views.status_extracao,
        name="status_extracao"
    ),

]