from django.urls import path
from . import views
urlpatterns = [
    path('index', views.index, name='index'),
    path('equipamento', views.selecionaEquipamento, name='equipamento'),
    path('problema', views.selecionaProblema, name='problema'),
    path('teste', views.preparaTeste, name='preparaTeste'),
    path('testeDetail', views.iniciaTeste, name='testeDetail'),
    path('pesquisa', views.pesquisa, name='pesquisa')
    #path('',views.getTeste, name='testes'),
]