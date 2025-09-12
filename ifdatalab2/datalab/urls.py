from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_redirect, name='home'),  # rota raiz
    path("dashboard-geral/", views.dashboard_geral, name='dashboard_geral'),
    path("dashboard/<int:grupo_id>/", views.dashboard_grupo, name="dashboard_grupo"),
    path("selecionar-grupo/", views.selecionar_grupo, name="selecionar_grupo"),
]
