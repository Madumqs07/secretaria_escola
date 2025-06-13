# Importa o módulo de formulários do Django
from django import forms
# Importa o modelo Contrato definido na aplicação
from .models import Contrato

# Formulário para marcar se o contrato foi assinado
class ContratoAssinadoForm(forms.ModelForm):
    class Meta:
        model = Contrato  # Define o modelo associado ao formulário
        fields = ['contrato_assinado']  # Campos do modelo que estarão disponíveis no formulário