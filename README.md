# Printer Monitor

Aplicação Django para gerenciar impressoras e acompanhar o nível de toner e o status de cada equipamento, com dados simulados para demonstração.

## Sobre o projeto

O Printer Monitor permite:

- Cadastrar impressoras (número de série, IP, setor)
- Consultar o nível de toner remanescente de cada impressora
- Editar e excluir impressoras cadastradas
- Autenticar usuários e gerenciar suas contas com acesso de superusuário
- Popular o banco com dados fictícios para demonstração, através de um comando customizado (`seed`)
- Receber alertas visuais (sino na navbar) quando o toner de alguma impressora estiver baixo, crítico ou esgotado
- Simular consumo de toner automaticamente ao longo do tempo, através de um agendador em segundo plano

> ⚠️ Todos os dados de exemplo usados neste repositório (IPs, números de série, setores) são **fictícios**. Os IPs pertencem a faixas reservadas pela IANA para documentação (RFC 5737) e nunca correspondem a endereços reais.
>
> ℹ️ O nível de toner de cada impressora é simulado: um agendador em segundo plano reduz o valor automaticamente a cada 15 minutos, simulando o desgaste de um cartucho real ao longo do tempo. Não há requisição de rede real às impressoras.

## Tecnologias

- Python / Django
- PostgreSQL
- Docker e Docker Compose
- Bootstrap 5 + Font Awesome
- APScheduler (agendamento automático)

## Como rodar o projeto

### Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados

### Passo a passo

1. Clone o repositório:

   ```bash
   git clone https://github.com/Cabral-JV/printer-monitor.git
   cd printer-monitor
   ```

1. Crie o arquivo de variáveis de ambiente a partir do exemplo:

   ```bash
   cp .env.example .env
   ```

   Edite o `.env` e ajuste os valores conforme necessário (por padrão, os valores de exemplo já funcionam para rodar localmente).

1. Suba os containers:

   ```bash
   docker compose up -d --build
   ```

1. Aplique as migrations:

   ```bash
   docker compose exec web python manage.py migrate
   ```

1. Crie um superusuário para gerenciar usuários e acessar o painel administrativo:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

1. Popule o banco com impressoras fictícias:

   ```bash
   docker compose exec web python manage.py seed
   ```

1. Acesse a aplicação em [http://localhost:8000](http://localhost:8000). A listagem de impressoras é pública; para cadastrar, editar ou excluir impressoras, entre com o usuário criado. O painel administrativo fica disponível em [http://localhost:8000/admin](http://localhost:8000/admin).

### Comandos úteis

| Comando | O que faz |
| --- | --- |
| `docker compose up -d` | Sobe os containers em segundo plano |
| `docker compose down` | Derruba os containers (os dados do banco são preservados) |
| `docker compose logs -f web` | Acompanha os logs do container Django em tempo real |
| `docker compose exec web python manage.py <comando>` | Roda qualquer comando do Django dentro do container |

## Rodando os testes

Com os containers em execução e o banco configurado, execute a suíte de testes:

```bash
docker compose exec web python manage.py test
```

Os testes abrangem o modelo de impressora, autenticação, operações de cadastro, edição e exclusão de impressoras e proteções na gestão de usuários.

Para executar apenas os testes do modelo de impressora (`test_models.py`), informe o caminho do módulo no comando:

```bash
docker compose exec web python manage.py test printer_monitor.tests.test_models
```

Para testar outra parte da aplicação, substitua `test_models` por um dos módulos abaixo, mantendo o prefixo `printer_monitor.tests.`:

| Módulo | O que testa |
| --- | --- |
| `test_auth` | Login e permissões de acesso |
| `test_printer_crud` | Cadastro, edição e exclusão de impressoras |
| `test_user_crud` | Proteções na gestão de usuários |

## Estrutura do projeto

```text
printer-monitor/
├── printer_monitor_project/       # Configuração global do Django
│   ├── settings.py               # Banco, autenticação, templates e apps
│   ├── urls.py                   # Rotas principais
│   ├── asgi.py                   # Entrada ASGI
│   └── wsgi.py                   # Entrada WSGI
├── printer_monitor/              # Aplicação principal
│   ├── management/commands/
│   │   └── seed.py               # Geração de impressoras fictícias
│   ├── migrations/               # Histórico do esquema do banco
│   ├── static/printer_monitor/css/
│   │   └── style.css             # Estilos da interface
│   ├── templates/
│   │   ├── printer_monitor/      # Layout e telas de impressoras e usuários
│   │   │   └── partials/         # Modais de impressoras
│   │   └── registration/         # Tela de login
│   ├── tests/
│   │   ├── test_auth.py          # Login e permissões de acesso
│   │   ├── test_models.py        # Modelo e consumo de toner
│   │   ├── test_printer_crud.py  # Cadastro, edição e exclusão de impressoras
│   │   └── test_user_crud.py     # Proteções na gestão de usuários
│   ├── admin.py                  # Integração com o painel administrativo
│   ├── apps.py                   # Configuração do app e início do agendador
│   ├── context_processors.py     # Alertas de toner nos templates
│   ├── forms.py                  # Formulários de impressoras e usuários
│   ├── models.py                 # Modelo Printer
│   ├── scheduler.py              # Agendamento da atualização de toner
│   ├── scraping.py               # Simulação de consumo de toner
│   ├── urls.py                   # Rotas da aplicação
│   └── views.py                  # Telas e operações de impressoras e usuários
├── .env.example                  # Exemplo de variáveis de ambiente
├── Dockerfile                    # Imagem da aplicação
├── docker-compose.yml            # Serviços da aplicação e PostgreSQL
├── manage.py                     # Comandos de gerenciamento do Django
└── requirements.txt              # Dependências Python
```

## Status do desenvolvimento

- [x] Estrutura inicial do projeto Django
- [x] Configuração de variáveis de ambiente
- [x] Dockerização
- [x] Model e migrations
- [x] Views, URLs e templates (CRUD completo)
- [x] Seed com dados fictícios
- [x] Autenticação (login/logout)
- [x] Gestão de usuários
- [x] Agendamento automático com simulação de consumo de toner
- [x] Sistema de notificações (alertas de toner na navbar)
- [x] Interface visual com Bootstrap
- [x] Testes automatizados
