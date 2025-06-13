from django.apps import AppConfig  # Importa a classe base para configuração de apps Django


# Classe de configuração do app 'secretaria'
class SecretariaConfig(AppConfig):
    # Define o tipo padrão de campo auto-incremento para chaves primárias
    default_auto_field = 'django.db.models.BigAutoField'
    # Nome do app, usado pelo Django para identificar este módulo
    name = 'secretaria'
