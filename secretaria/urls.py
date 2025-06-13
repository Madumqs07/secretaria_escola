from django.urls import path
from . import views

# Rotas específicas da aplicação secretaria
urlpatterns = [
    path('gerar-contrato/<int:aluno_id>/', views.gerar_contrato_pdf, name='gerar_contrato_pdf'),
    path('aluno/<int:aluno_id>/adicionar-nota/', views.adicionar_nota, name='adicionar_nota'),
    path('aluno/<int:aluno_id>/boletim/', views.ver_boletim, name='ver_boletim'),
    path('aluno/<int:aluno_id>/boletim_pdf/', views.gerar_boletim_pdf, name='boletim_pdf'),
    path('aluno/<int:aluno_id>/', views.aluno_detalhe, name='aluno_detalhe'),
    path('boletins_pdf_todos/', views.gerar_boletins_pdf_todos_alunos, name='boletins_pdf_todos'),
    path('aluno/<int:aluno_id>/desempenho/', views.desempenho, name='desempenho'),
]