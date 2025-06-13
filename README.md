# Sistema de Gestão Escolar - Secretaria

Este projeto é um sistema web desenvolvido em Django para a gestão escolar, focado na secretaria da escola. Ele permite o gerenciamento de alunos, responsáveis, professores, turmas, contratos, disciplinas e notas, além da geração de relatórios e contratos em PDF.

## Funcionalidades principais

- **Cadastro de Alunos, Responsáveis e Professores:**
  - Armazena dados completos, como nome, telefone, e-mail, CPF e data de nascimento.
  - Relaciona alunos a responsáveis.

- **Gestão de Turmas e Disciplinas:**
  - Cadastro de turmas com padrinho, representante e itinerário.
  - Cadastro de disciplinas.

- **Notas e Boletins:**
  - Lançamento de notas por disciplina para cada aluno.
  - Visualização do boletim do aluno e geração de boletim em PDF.
  - Geração de boletins em PDF para todos os alunos (ZIP).

- **Contratos:**
  - Geração de contrato personalizado em PDF para cada aluno, com dados do responsável selecionado.
  - Upload e armazenamento de contratos assinados.
  - Visualização do contrato gerado e do contrato assinado (se houver).

- **Desempenho:**
  - Exibição de gráficos de desempenho do aluno e da turma.
  - Upload de contrato assinado diretamente na tela de desempenho.

## Estrutura do Projeto

- `secretaria/models.py`: Modelos de dados (Aluno, Responsavel, Professor, Turma, Contrato, Disciplina, Nota).
- `secretaria/views.py`: Lógica das views para cadastro, geração de PDFs, desempenho, etc.
- `secretaria/forms.py`: Formulários para upload de contrato assinado.
- `secretaria/urls.py`: Rotas da aplicação secretaria.
- `templates/`: Templates HTML para as páginas do sistema.
- `media/contratos_assinados/`: Onde ficam armazenados os contratos assinados enviados.

## Como funciona a geração de contrato

Na aba "Contratos", o usuário seleciona o aluno e o responsável. O sistema gera um PDF de contrato personalizado com os dados selecionados, disponível para visualização e download.

## Como rodar o projeto

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
3. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```
4. Acesse em `http://localhost:8000/`

---

Este sistema é ideal para escolas que desejam digitalizar e automatizar processos de secretaria, contratos e acompanhamento pedagógico.
