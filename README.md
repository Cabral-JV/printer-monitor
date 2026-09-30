# Printer Monitor

Aplicação Django para monitorar o nível de toner e status de impressoras em rede.

## Sobre o projeto

O Printer Monitor permite:

- Cadastrar impressoras (número de série, IP, setor)
- Consultar o nível de toner remanescente de cada impressora
- Editar e excluir impressoras cadastradas
- Popular o banco com dados fictícios para demonstração, através de um comando customizado (`seed`)
- Receber alertas visuais (sino na navbar) quando o toner de alguma impressora estiver baixo, crítico ou esgotado
- Simular consumo de toner automaticamente ao longo do tempo, através de um agendador em segundo plano

> ⚠️ Todos os dados de exemplo usados neste repositório (IPs, números de série, setores) são **fictícios**. Os IPs pertencem a faixas reservadas pela IANA para documentação (RFC 5737) e nunca correspondem a endereços reais.
>
> ℹ️ O nível de toner de cada impressora é simulado: um agendador em segundo plano reduz o valor automaticamente a cada poucos minutos, simulando o desgaste de um cartucho real ao longo do tempo. Não há requisição de rede real às impressoras.

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

1. (Opcional) Crie um superusuário para acessar o painel administrativo:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

1. Popule o banco com impressoras fictícias:

   ```bash
   docker compose exec web python manage.py seed
   ```

1. Acesse a aplicação em [http://localhost:8000](http://localhost:8000). O painel administrativo fica disponível em [http://localhost:8000/admin](http://localhost:8000/admin).

### Comandos úteis

| Comando | O que faz |
| --- | --- |
| `docker compose up -d` | Sobe os containers em segundo plano |
| `docker compose down` | Derruba os containers (os dados do banco são preservados) |
| `docker compose logs -f web` | Acompanha os logs do container Django em tempo real |
| `docker compose exec web python manage.py <comando>` | Roda qualquer comando do Django dentro do container |

## Estrutura do projeto

```text
printer-monitor/
├── printer_monitor_project/ # Configurações do projeto (settings, urls raiz)
├── printer_monitor/ # App principal
│ ├── management/commands/ # Comando customizado "seed"
│ ├── migrations/ # Histórico do esquema do banco
│ ├── templates/ # Templates HTML
│ ├── models.py # Model Printer
│ ├── views.py # Views (CRUD de impressoras)
│ ├── forms.py # Formulário de cadastro/edição
│ └── urls.py # Rotas do app
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
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
- [ ] Testes automatizados
