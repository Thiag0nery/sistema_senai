from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('importar_csv/', views.importar_csv, name='importar_csv'),
    path('salvar_hora/', views.salvar_hora, name='salvar_hora'),
    path('redirecionar-para-admin/', views.redirecionar_para_admin, name='redirecionar_para_admin'),
    path('user_authentication', views.user_authentication, name='user_authentication'),
    path('pesquisa', views.pesquisa, name='pesquisa')
]
