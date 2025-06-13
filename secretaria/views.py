from django.shortcuts import render, get_object_or_404, redirect
# secretaria/views.py

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Aluno, Nota, Disciplina, Contrato, Responsavel
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.files.base import ContentFile
import os
import io
import zipfile
from django.views.decorators.csrf import csrf_exempt
import base64

# Gera um PDF de contrato para um aluno específico
def gerar_contrato_pdf(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    responsavel_id = request.GET.get('responsavel_id')
    if responsavel_id:
        responsavel = get_object_or_404(Responsavel, id=responsavel_id)
    else:
        responsavel = getattr(aluno, 'responsavel', None)

    # Monta o contexto com dados do aluno e do responsável
    context = {
        'aluno': {
            'nome': aluno.aluno_name_complete,
            'data_nascimento': aluno.birthday_aluno.strftime('%d/%m/%Y'),
            'cpf': aluno.cpf_aluno,
            'telefone': aluno.phone_number_aluno,
            'email': aluno.email_aluno,
        },
        'responsavel': {
            'nome': responsavel.complete_name if responsavel else '',
            'data_nascimento': responsavel.birthday.strftime('%d/%m/%Y') if responsavel and responsavel.birthday else '',
            'cpf': responsavel.cpf if responsavel else '',
            'telefone': responsavel.phone_number if responsavel else '',
            'email': responsavel.email if responsavel else '',
            'endereco': responsavel.adress if responsavel else '',
        }
    }

    # Renderiza o HTML e gera o PDF
    html_string = render_to_string('contrato.html', context)
    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contrato_{aluno.aluno_name_complete}.pdf"'
    return response

# Adiciona uma nota para um aluno em uma disciplina
def adicionar_nota(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    disciplinas = Disciplina.objects.all()
    if request.method == 'POST':
        disciplina_id = request.POST.get('disciplina')
        valor = request.POST.get('valor')
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            valor = None
        # Validação do valor da nota
        if valor is None or valor < 0 or valor > 10:
            return render(request, 'adicionar_nota.html', {'aluno': aluno, 'disciplinas': disciplinas, 'erro': 'A nota deve ser entre 0 e 10.'})
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        Nota.objects.create(aluno=aluno, disciplina=disciplina, valor=valor)
        return redirect(reverse('ver_boletim', args=[aluno.id]))
# Exibe o boletim do aluno, agrupando notas por disciplina
def ver_boletim(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    notas = Nota.objects.filter(aluno=aluno).select_related('disciplina')
    # Organiza as notas por disciplina
    boletim = {}
    for nota in notas:
        nome_disciplina = nota.disciplina.nome
        if nome_disciplina not in boletim:
            boletim[nome_disciplina] = []
        boletim[nome_disciplina].append(nota)
    return render(request, 'boletim.html', {'aluno': aluno, 'boletim': boletim})

# Exibe detalhes do aluno e permite adicionar nota via POST
def aluno_detalhe(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    disciplinas = Disciplina.objects.all()
    if request.method == 'POST':
        disciplina_id = request.POST.get('disciplina')
        valor = request.POST.get('valor')
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        Nota.objects.create(aluno=aluno, disciplina=disciplina, valor=valor)
        return redirect(reverse('aluno_detalhe', args=[aluno.id]))
    return render(request, 'aluno_detalhe.html', {'aluno': aluno, 'disciplinas': disciplinas})

# Gera um PDF do boletim do aluno, incluindo notas por disciplina
def gerar_boletim_pdf(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    notas = Nota.objects.filter(aluno=aluno).select_related('disciplina')
    # Organiza as notas por disciplina
    boletim = {}
    for nota in notas:
        nome_disciplina = nota.disciplina.nome
        if nome_disciplina not in boletim:
            boletim[nome_disciplina] = []
        boletim[nome_disciplina].append(nota)

    from io import BytesIO
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Cabeçalho do boletim
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Boletim Escolar - {aluno.aluno_name_complete}")

    p.setFont("Helvetica", 12)
    responsavel = getattr(aluno, 'responsavel', None)
    responsavel_nome = responsavel.complete_name if responsavel else ""
    turma = aluno.get_class_choices_display() if hasattr(aluno, 'get_class_choices_display') else str(aluno.class_choices)
    p.drawString(50, height - 80, f"Turma: {turma}")
    p.drawString(50, height - 100, f"Responsável: {responsavel_nome}")

    y = height - 140
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Disciplina")
    p.drawString(300, y, "Nota(s)")
    y -= 20
    p.setFont("Helvetica", 12)

    # Lista de matérias básicas
    materias_basicas = ["Português", "Matemática", "História", "Geografia", "Ciências", "Inglês", "Educação Física", "Artes"]

    # Preenche as notas das matérias básicas
    for materia in materias_basicas:
        p.drawString(50, y, materia)
        notas_materia = boletim.get(materia, [])
        if notas_materia:
            notas_str = ", ".join([
                f"{nota.valor} ({nota.data.strftime('%d/%m/%Y')})"
                if hasattr(nota, 'data') and getattr(nota, 'data', None) else str(nota.valor)
                for nota in notas_materia
            ])
        else:
            notas_str = "Sem nota"
        p.drawString(300, y, notas_str)
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    # Outras disciplinas que não são básicas
    outras_disciplinas = [d for d in boletim.keys() if d not in materias_basicas]
    if outras_disciplinas:
        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Outras Disciplinas")
        y -= 20
        p.setFont("Helvetica", 12)
        for disciplina in outras_disciplinas:
            p.drawString(50, y, disciplina)
            notas_materia = boletim[disciplina]
            notas_str = ", ".join([
                f"{nota.valor} ({nota.data.strftime('%d/%m/%Y')})"
                if hasattr(nota, 'data') and getattr(nota, 'data', None) else str(nota.valor)
                for nota in notas_materia
            ])
            p.drawString(300, y, notas_str)
            y -= 20
            if y < 50:
                p.showPage()
                y = height - 50

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="boletim_{aluno.aluno_name_complete}.pdf"'
    return response

# Gera um arquivo ZIP contendo os boletins em PDF de todos os alunos
def gerar_boletins_pdf_todos_alunos(request):
    alunos = Aluno.objects.all()
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    import io
    
    zip_buffer = io.BytesIO()
    import zipfile
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for aluno in alunos:
            notas = Nota.objects.filter(aluno=aluno).select_related('disciplina')
            boletim = {}
            for nota in notas:
                nome_disciplina = nota.disciplina.nome
                if nome_disciplina not in boletim:
                    boletim[nome_disciplina] = []
                boletim[nome_disciplina].append(nota)

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, height - 50, f"Boletim Escolar - {aluno.aluno_name_complete}")
            p.setFont("Helvetica", 12)
            turma = aluno.get_class_choices_display() if hasattr(aluno, 'get_class_choices_display') else str(aluno.class_choices)
            responsavel_nome = aluno.responsavel.complete_name if hasattr(aluno, 'responsavel') and aluno.responsavel else ""
            p.drawString(50, height - 80, f"Turma: {turma}")
            p.drawString(50, height - 100, f"Responsável: {responsavel_nome}")
            y = height - 140
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y, "Disciplina")
            p.drawString(300, y, "Nota(s)")
            y -= 20
            p.setFont("Helvetica", 12)
            materias_basicas = ["Português", "Matemática", "História", "Geografia", "Ciências", "Inglês", "Educação Física", "Artes"]
            for materia in materias_basicas:
                p.drawString(50, y, materia)
                notas_materia = boletim.get(materia, [])
                if notas_materia:
                    notas_str = ", ".join([
                        f"{nota.valor} ({nota.data.strftime('%d/%m/%Y')})"
                        if hasattr(nota, 'data') and getattr(nota, 'data', None) else str(nota.valor)
                        for nota in notas_materia
                    ])
                else:
                    notas_str = "Sem nota"
                p.drawString(300, y, notas_str)
                y -= 20
                if y < 50:
                    p.showPage()
                    y = height - 50
            outras_disciplinas = [d for d in boletim.keys() if d not in materias_basicas]
            if outras_disciplinas:
                y -= 20
                p.setFont("Helvetica-Bold", 12)
                p.drawString(50, y, "Outras Disciplinas")
                y -= 20
                p.setFont("Helvetica", 12)
                for disciplina in outras_disciplinas:
                    p.drawString(50, y, disciplina)
                    notas_materia = boletim[disciplina]
                    notas_str = ", ".join([
                        f"{nota.valor} ({nota.data.strftime('%d/%m/%Y')})"
                        if hasattr(nota, 'data') and getattr(nota, 'data', None) else str(nota.valor)
                        for nota in notas_materia
                    ])
                    p.drawString(300, y, notas_str)
                    y -= 20
                    if y < 50:
                        p.showPage()
                        y = height - 50
            p.showPage()
            p.save()
            pdf_data = buffer.getvalue()
            buffer.close()
            filename = f"boletim_{aluno.aluno_name_complete.replace(' ', '_')}.pdf"
            zip_file.writestr(filename, pdf_data)
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="boletins_alunos.zip"'
    return response

# Exibe gráficos de desempenho do aluno e da turma
def desempenho(request, aluno_id=None):
    aluno = None
    contratos = []
    if aluno_id:
        aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST' and request.FILES.get('contrato_assinado'):
        from .forms import ContratoAssinadoForm
        form = ContratoAssinadoForm(request.POST, request.FILES)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.aluno = aluno
            contrato.save()
            return redirect('desempenho', aluno_id=aluno.id)
    if aluno:
        contratos = Contrato.objects.filter(aluno=aluno)
    # Gráfico do aluno: média por disciplina
    labels_aluno = []
    dados_aluno = []
    boletim = {}
    for nota in Nota.objects.filter(aluno=aluno).select_related('disciplina') if aluno else []:
        nome_disciplina = nota.disciplina.nome
        if nome_disciplina not in boletim:
            boletim[nome_disciplina] = []
        boletim[nome_disciplina].append(nota.valor)
    for disciplina, valores in boletim.items():
        labels_aluno.append(disciplina)
        dados_aluno.append(sum(valores) / len(valores) if valores else 0)
    materias = Disciplina.objects.all()
    dados_materia = {}
    for materia in materias:
        notas_materia = Nota.objects.filter(aluno=aluno, disciplina=materia).order_by('id') if aluno else []
        dados_materia[materia.nome] = [nota.valor for nota in notas_materia]
    turma = aluno.class_choices if aluno else None
    alunos_turma = Aluno.objects.filter(class_choices=turma) if turma else []
    labels_turma = []
    dados_turma = []
    for a in alunos_turma:
        notas_a = Nota.objects.filter(aluno=a)
        if notas_a.exists():
            media = sum([n.valor for n in notas_a]) / notas_a.count()
            labels_turma.append(a.aluno_name_complete)
            dados_turma.append(media)
    context = {
        'aluno': aluno,
        'labels_aluno': labels_aluno,
        'dados_aluno': dados_aluno,
        'dados_materia': dados_materia,
        'labels_turma': labels_turma,
        'dados_turma': dados_turma,
        'contratos': contratos,
    }
    return render(request, 'desempenho.html', context)

# Views da aplicação secretaria: geração de PDFs, exibição de boletins, desempenho, etc.

# Exibe a lista de alunos para seleção e visualização do contrato em PDF
def contratos(request):
    alunos = Aluno.objects.all()
    responsaveis = Responsavel.objects.all()
    aluno_id = request.GET.get('aluno_id')
    responsavel_id = request.GET.get('responsavel_id')
    aluno_selecionado = None
    responsavel_selecionado = None
    if aluno_id:
        aluno_selecionado = Aluno.objects.filter(id=aluno_id).first()
    if responsavel_id:
        responsavel_selecionado = Responsavel.objects.filter(id=responsavel_id).first()
    # Gera a URL para o contrato em PDF, se aluno e responsável estiverem selecionados
    if aluno_id and responsavel_id:
        contrato_url = reverse('gerar_contrato_pdf', args=[aluno_id]) + f'?responsavel_id={responsavel_id}'
    else:
        contrato_url = None
    return render(request, 'contratos.html', {
        'alunos': alunos,
        'responsaveis': responsaveis,
        'aluno_id': aluno_id,
        'responsavel_id': responsavel_id,
        'contrato_url': contrato_url,
        'aluno_selecionado': aluno_selecionado,
        'responsavel_selecionado': responsavel_selecionado,
    })
