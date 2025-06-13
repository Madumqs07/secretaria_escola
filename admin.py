from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

class DesempenhoAdminView(admin.ModelAdmin):
    change_list_template = "admin/desempenho_dashboard.html"

    def changelist_view(self, request, extra_context=None):
        # Aqui você pode buscar e processar os dados de desempenho
        context = {
            # Adicione dados de desempenho do aluno, matéria e turma
            # Exemplo:
            # 'alunos': Aluno.objects.all(),
            # 'turmas': Turma.objects.all(),
            # 'materias': Materia.objects.all(),
        }
        return TemplateResponse(request, "admin/desempenho_dashboard.html", context)