from django.urls import path
from . import views

app_name = 'datalab'

urlpatterns = [
    path('', views.dashboard_geral, name='dashboard_geral'),
]
