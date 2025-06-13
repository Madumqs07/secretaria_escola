"""
Configuração de URLs para o projeto App_escola.

Este arquivo define as rotas principais do projeto, direcionando as URLs para os módulos corretos.

- admin/: Acesso ao painel administrativo do Django.
- secretaria/: Inclui todas as rotas do app secretaria (alunos, notas, desempenho, etc).

Para adicionar uma página inicial personalizada, basta descomentar a importação e a linha correspondente no urlpatterns.
"""

from django.contrib import admin  # Importa o módulo de administração padrão do Django
from django.urls import path, include  # Importa funções para definir rotas e incluir URLs de outros apps
from django.conf import settings
from django.conf.urls.static import static
# from secretaria.views import home  # Import da view home (página inicial) - descomente se quiser uma página inicial customizada

# Lista de padrões de URL do projeto
urlpatterns = [
    # path('', home, name='home'),  # Página inicial do sistema. Descomente e ajuste a view para ativar uma home page.
    path('admin/', admin.site.urls),  # Rota para o painel administrativo do Django (ex: /admin/)
    path('secretaria/', include('secretaria.urls')),  # Inclui todas as rotas do app secretaria (ex: /secretaria/aluno/, /secretaria/nota/, etc)
]

# Servir arquivos de mídia em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

