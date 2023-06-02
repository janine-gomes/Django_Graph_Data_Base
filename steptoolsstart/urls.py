from django.urls import path
from . import views
urlpatterns = [
    path('index', views.index, name='index'),
    path('equipamento', views.selecionaEquipamento, name='equipamento'),
    path('problema', views.selecionaProblema, name='problema'),
    path('confirmadados', views.coletaDadosTeste, name='confirmadados'),
    path('teste', views.iniciaTeste, name='teste'),
    path('pesquisa', views.pesquisa, name='pesquisa')
]