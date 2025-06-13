import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Script utilitário para geração de relatórios PDF com gráficos de desempenho dos alunos

# Gera um gráfico de barras com as médias das notas por matéria e salva como imagem
# medias: lista de médias das notas
# materias: lista com os nomes das matérias
# caminho_img: caminho do arquivo de imagem a ser salvo
def gerar_grafico_medias(medias, materias, caminho_img):
    plt.figure(figsize=(6,4))
    plt.bar(materias, medias, color='skyblue')
    plt.xlabel('Matérias')
    plt.ylabel('Média das Notas')
    plt.title('Média das Notas por Matéria')
    plt.tight_layout()
    plt.savefig(caminho_img)
    plt.close()

# Gera um gráfico de linha mostrando o desempenho geral do aluno nas matérias
# materias: lista com os nomes das matérias
# medias: lista de médias das notas
# caminho_img: caminho do arquivo de imagem a ser salvo
def gerar_grafico_desempenho(materias, medias, caminho_img):
    plt.figure(figsize=(6,4))
    plt.plot(materias, medias, marker='o', color='green', label='Desempenho')
    plt.xlabel('Matérias')
    plt.ylabel('Média das Notas')
    plt.title('Gráfico de Desempenho do Aluno')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho_img)
    plt.close()

# Gera um gráfico de linha para o desempenho do aluno em uma matéria específica
# materia: nome da matéria
# notas: lista de notas do aluno na matéria
# caminho_img: caminho do arquivo de imagem a ser salvo
def gerar_grafico_materia(materia, notas, caminho_img):
    plt.figure(figsize=(4,2.5))
    plt.plot(range(1, len(notas)+1), notas, marker='o', color='blue')
    plt.title(f'Desempenho em {materia}')
    plt.xlabel('Avaliação')
    plt.ylabel('Nota')
    plt.ylim(0, 10)
    plt.tight_layout()
    plt.savefig(caminho_img)
    plt.close()

# Gera um PDF contendo os gráficos e as informações de notas do aluno
# aluno: nome do aluno
# turma: nome da turma
# materias: lista de matérias
# notas: lista de listas de notas por matéria
# caminho_pdf: caminho do arquivo PDF a ser salvo
def gerar_pdf(aluno, turma, materias, notas, caminho_pdf):
    medias = [sum(n)/len(n) for n in notas]
    caminho_img_medias = "grafico_medias.png"
    caminho_img_desempenho = "grafico_desempenho.png"
    gerar_grafico_medias(medias, materias, caminho_img_medias)
    gerar_grafico_desempenho(materias, medias, caminho_img_desempenho)

    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Boletim Escolar com Gráficos de Desempenho")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Aluno: {aluno}")
    c.drawString(50, height - 110, f"Turma: {turma}")

    y = height - 150
    for i, materia in enumerate(materias):
        media = sum(notas[i])/len(notas[i])
        c.drawString(50, y, f"Matéria: {materia} | Notas: {notas[i]} | Média: {media:.2f}")
        # Gerar gráfico individual da matéria
        caminho_img = f"grafico_{materia}.png"
        gerar_grafico_materia(materia, notas[i], caminho_img)
        y -= 20
        c.drawImage(caminho_img, 50, y-80, width=250, height=120)
        y -= 130  # Espaço após o gráfico

        if y < 150:  # Nova página se necessário
            c.showPage()
            y = height - 50

    c.save()

# Exemplo de uso para testar a geração do PDF e gráficos
if __name__ == "__main__":
    aluno = "Lucas Marques"
    turma = "3DS"
    materias = ["Matemática", "Português", "História"]
    notas = [
        [8, 7, 9],   # Matemática
        [6, 7, 8],   # Português
        [9, 8, 10]   # História
    ]
    gerar_pdf(aluno, turma, materias, notas, "relatorio_desempenho.pdf")
