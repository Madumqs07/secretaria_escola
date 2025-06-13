from django.contrib import admin  # Importa o módulo de administração do Django
from secretaria.models import *  # Importa todos os modelos do app secretaria

# Configuração do admin para o modelo Responsavel
class ResponsaveisAdmin(admin.ModelAdmin):
    list_display = ('id', 'complete_name', 'phone_number', 'email', 'adress', 'cpf', 'birthday')  # Colunas exibidas na lista
    list_display_links = ('complete_name', 'phone_number', 'email', 'adress', 'cpf', 'birthday')  # Campos clicáveis
    search_fields = ('complete_name',)  # Campo de busca
    list_filter = ('complete_name',)  # Filtro lateral

# Configuração do admin para o modelo Aluno
class AlunosAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno_name_complete', 'phone_number_aluno', 'email_aluno', 'cpf_aluno', 'birthday_aluno', 'class_choices', 'contrato_pdf_link', 'boletim_pdf_link')  # Colunas exibidas
    list_display_links = ('aluno_name_complete', 'phone_number_aluno', 'email_aluno', 'cpf_aluno', 'birthday_aluno', 'class_choices')  # Campos clicáveis
    search_fields = ('aluno_name_complete',)  # Campo de busca
    list_filter = ('aluno_name_complete',)  # Filtro lateral

    # Adiciona botão para gerar contrato PDF diretamente no admin
    def contrato_pdf_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        if obj.id:
            url = reverse('gerar_contrato_pdf', args=[obj.id])
            return format_html(f'<a class="button" href="{url}" target="_blank">📄 Gerar Contrato</a>')
        return "-"
    contrato_pdf_link.short_description = "Contrato em PDF"

    # Adiciona botão para gerar boletim PDF diretamente no admin
    def boletim_pdf_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        if obj.id:
            url = reverse('boletim_pdf', args=[obj.id])
            return format_html(f'<a class="button" href="{url}" target="_blank">📊 Boletim PDF</a>')
        return "-"
    boletim_pdf_link.short_description = "Boletim em PDF"

# Configuração do admin para o modelo Professor
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_completo_professor', 'phone_number_professor', 'email_professor', 'cpf_professor', 'birthday_professor', 'padrinho_turma_professores')
    list_display_links = ('nome_completo_professor', 'phone_number_professor', 'email_professor', 'cpf_professor', 'birthday_professor', 'padrinho_turma_professores')
    search_fields = ('nome_completo_professor',)
    list_filter = ('nome_completo_professor',)

# Configuração do admin para o modelo Turma
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma_name', 'intinerario_name', 'padrinho_name', 'representante_name', 'escolha_a_turma', 'intinerario_choice')
    list_display_links = ('turma_name', 'intinerario_name', 'padrinho_name', 'representante_name', 'escolha_a_turma', 'intinerario_choice')
    search_fields = ('turma_name', 'intinerario_name',)
    list_filter = ('turma_name', 'intinerario_name',)

# Configuração do admin para o modelo Contrato
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'contrato_assinado')  # Exibe o aluno e se o contrato está assinado
    list_filter = ('aluno',)  # Filtro lateral por aluno

# Configuração do admin para o modelo Disciplina
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)

# Configuração do admin para o modelo Nota
class NotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'disciplina', 'valor', 'data')
    search_fields = ('aluno__aluno_name_complete', 'disciplina__nome')
    list_filter = ('disciplina', 'aluno')

# Registro dos modelos e suas configurações no painel administrativo do Django
admin.site.register(Responsavel, ResponsaveisAdmin)
admin.site.register(Aluno, AlunosAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Nota, NotaAdmin)