from django.db import models
from .validador import telefone_validator, validar_cpf

# Modelo para armazenar informações do responsável pelo aluno
class Responsavel(models.Model):
    complete_name = models.CharField(max_length=100, null=True)  # Nome completo do responsável
    phone_number = models.CharField(max_length=15, verbose_name="Digite o N° do celular (xx) xxxxx-xxxx", validators=[telefone_validator])  # Telefone com validador
    email = models.EmailField(max_length=100, verbose_name="E-mail do responsavel")  # E-mail do responsável
    adress = models.CharField(max_length=100)  # Endereço do responsável
    cpf = models.CharField(max_length=11, unique=True, verbose_name="Informe o CPF do Responsavel", validators=[validar_cpf])  # CPF com validador
    birthday = models.DateField()  # Data de nascimento

    def __str__(self):
        # Retorna o nome completo ao exibir o objeto
        return self.complete_name
    
# Modelo para armazenar informações do aluno
class Aluno(models.Model):
    # Opções de turma disponíveis
    TURMA_CHOICES = (
        ("1A", "1° Ano A"),
        ("1B", "1° Ano B"),
        ("1C", "1° Ano C"),
        ("2A", "2° Ano A"),
        ("2B", "2° Ano B"),
        ("2C", "2° Ano C"),
        ("3A", "3° Ano A"),
        ("3B", "3° Ano B"),
        ("3C", "3° Ano C"),
    )

    aluno_name_complete = models.CharField(max_length=100, null=True, verbose_name="Digite o nome completo do aluno")  # Nome completo do aluno
    phone_number_aluno = models.CharField(max_length=15, verbose_name="Digite o N° do celular (xx) xxxxx-xxxx", validators=[telefone_validator])  # Telefone do aluno
    email_aluno = models.EmailField(max_length=100, verbose_name="E-mail do aluno")  # E-mail do aluno
    cpf_aluno = models.CharField(max_length=11, unique=True, verbose_name="Informe o CPF do aluno", validators=[validar_cpf])  # CPF do aluno
    birthday_aluno = models.DateField()  # Data de nascimento do aluno
    class_choices = models.CharField(max_length=2, choices=TURMA_CHOICES, blank=True, null=False)  # Turma do aluno
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, null=True, blank=True, related_name="alunos")  # Relação com o responsável

    def __str__(self):
        # Retorna o nome completo ao exibir o objeto
        return self.aluno_name_complete

# Modelo para armazenar informações do professor
class Professor(models.Model):
    TURMA_CHOICES = (
        ("1A", "1° Ano A"),
        ("1B", "1° Ano B"),
        ("1C", "1° Ano C"),
        ("2A", "2° Ano A"),
        ("2B", "2° Ano B"),
        ("2C", "2° Ano C"),
        ("3A", "3° Ano A"),
        ("3B", "3° Ano B"),
        ("3C", "3° Ano C"),
    )
    
    nome_completo_professor = models.CharField(max_length=50, null=True, verbose_name="Digite o nome do professor")  # Nome completo do professor
    phone_number_professor = models.CharField(max_length=15, verbose_name="Digite o N° do celular (xx) xxxxx-xxxx", validators=[telefone_validator])  # Telefone do professor
    email_professor = models.EmailField(max_length=100, verbose_name="E-mail do professor")  # E-mail do professor
    cpf_professor = models.CharField(max_length=11, unique=True, verbose_name="Informe o CPF do professor", validators=[validar_cpf])  # CPF do professor
    birthday_professor = models.DateField()  # Data de nascimento do professor
    padrinho_turma_professores = models.CharField(max_length=2, choices=TURMA_CHOICES, blank=True, null=False)  # Turma apadrinhada

    def __str__(self):
        # Retorna o nome completo ao exibir o objeto
        return self.nome_completo_professor
    
# Modelo para armazenar informações das turmas
class Turma(models.Model):
    TURMA_CHOICES = (
        ("1A", "1° Ano A"),
        ("1B", "1° Ano B"),
        ("1C", "1° Ano C"),
        ("2A", "2° Ano A"),
        ("2B", "2° Ano B"),
        ("2C", "2° Ano C"),
        ("3A", "3° Ano A"),
        ("3B", "3° Ano B"),
        ("3C", "3° Ano C"),
    )
    INTINERARIO_CHOICES = (
        ("D.S.", "Desenvolvimento de Sistemas"),
        ("C.N.", "Ciencias da Natureza"),
        ("Jogos", "Jogos Digitais"),
    )
    turma_name = models.CharField(max_length=50)  # Nome da turma
    intinerario_name = models.CharField(max_length=50)  # Nome do itinerário
    padrinho_name = models.CharField(max_length=50)  # Nome do padrinho da turma
    representante_name = models.CharField(max_length=50)  # Nome do representante da turma
    escolha_a_turma = models.CharField(max_length=2, choices=TURMA_CHOICES, blank=True, null=False)  # Escolha da turma
    intinerario_choice = models.CharField(max_length=8, choices=INTINERARIO_CHOICES, blank=True, null=False)  # Escolha do itinerário

    def __str__(self):
        # Retorna o nome da turma ao exibir o objeto
        return self.turma_name
    
# Modelo para armazenar contratos assinados dos alunos
class Contrato(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)  # Relação com o aluno
    contrato_assinado = models.FileField(upload_to='contratos_assinados/', null=True, blank=True)  # Arquivo do contrato assinado

    def __str__(self):
        # Retorna uma string identificando o contrato pelo nome do aluno
        return f"Contrato de {self.aluno.aluno_name_complete}"
    
# Modelo para armazenar disciplinas
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)  # Nome da disciplina

    def __str__(self):
        # Retorna o nome da disciplina ao exibir o objeto
        return self.nome

# Modelo para armazenar notas dos alunos em disciplinas
class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')  # Relação com o aluno
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)  # Relação com a disciplina
    valor = models.DecimalField(max_digits=5, decimal_places=2)  # Valor da nota
    data = models.DateField(auto_now_add=True)  # Data de lançamento da nota

    def __str__(self):
        # Retorna uma string com o aluno, disciplina e valor da nota
        return f"{self.aluno} - {self.disciplina}: {self.valor}"

# Modelos da aplicação secretaria: Aluno, Professor, Turma, Contrato, Disciplina, Nota, Responsavel