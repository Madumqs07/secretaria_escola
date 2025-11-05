🤝 Como Contribuir com este Projeto de Secretaria Escolar
Ficamos muito felizes por você se interessar em contribuir! 
Este sistema é construído com Python/Django no backend. Para garantir que tudo corra bem, pedimos que siga estas diretrizes.

🛠️ Configuração do Ambiente (Pré-requisito)
Antes de enviar qualquer código, certifique-se de que seu ambiente de desenvolvimento está configurado:

Clone e Crie um Ambiente Virtual:

Bash

git clone [LINK DO REPOSITÓRIO]
cd nome-do-projeto
python -m venv venv
source venv/bin/activate  # Ou .\venv\Scripts\activate no Windows
Instale as Dependências:

Bash

pip install -r requirements.txt
Migrações: Execute as migrações do Django: python manage.py migrate.

🐛 Reportando Bugs
Se você encontrar um bug, por favor, abra uma "Issue" no repositório. No seu reporte, inclua:

Uma descrição clara do problema.

Passos para reproduzir o bug (Ex: "Na tela de Notas, ao clicar em Salvar com campo vazio...").

O que você esperava que acontecesse.

O que realmente aconteceu (com prints, se possível).

💡 Sugerindo Novas Funcionalidades (Features)
Abra uma "Issue" com o título "Feature: [Nome da sua ideia]".

Descreva a funcionalidade que você gostaria de ver (ex: Módulo de controle de material didático) e por que ela seria útil para a secretaria.

🚀 Enviando Mudanças (Pull Requests - PRs)
Para submeter código (correções ou novas funcionalidades), siga estes passos:

Faça um "Fork" deste repositório.

Crie um novo branch para suas mudanças. Recomendamos um prefixo claro:

Para correções: git checkout -b bugfix/descricao-curta-do-bug

Para novas features: git checkout -b feature/nome-da-feature

Faça suas alterações e "commits" com mensagens claras (preferencialmente seguindo o padrão Conventional Commits, ex: fix:, feat:).

Envie suas mudanças (git push) para o seu fork.

Abra um "Pull Request" (PR) para o branch main do nosso repositório principal.

Diretriz Técnica: Sempre que adicionar lógica de negócio nova ou corrigir um bug crítico em um Model ou View do Django, inclua um teste unitário correspondente.

Obrigado por sua contribuição!
