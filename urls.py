from django.urls import path
from .admin import DesempenhoAdminView

# Arquivo de rotas principal do projeto Django
# Inclua aqui as rotas globais e os includes das apps

# Lista de URLs principais do projeto
urlpatterns = [
    # ...existing code...
    # Rota para acessar a visualização de desempenho no admin
    path('admin/desempenho/', DesempenhoAdminView.as_view(), name='admin-desempenho'),
]