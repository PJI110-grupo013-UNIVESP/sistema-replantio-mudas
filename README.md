# PJI110 GRUPO 13 UNIVESP
Repositório para o Projeto Integrador da Univesp.

---

# 🌱 Sistema para Gestão e Monitoramento de Replantio de Mudas
Este projeto é uma aplicação Web desenvolvida como parte do Projeto Integrador. O Objetivo principal é fornecer uma solução tecnológica para a gestão e otimização de processos agrícolas e ambientais, focando especificamente no controle e monitoramento do processo de raplantio de mudas.

O sistema visa substituir controles manuais ou planilhas descentralizadas, centralizando dados importantes para a tomada de decisão no campo e garantindo um acompanhamento eficiente das etapas de cultivo.

## Funcionalidades Principais
* **Gestão do Viveiro/Mudas:** Cadastros de espécies, lotes, fornecedores e controle de estoque.
* **Controle de Replantio:** Registro de áreas de plantio, datas, responsáveis e taxa de mortalidade/Sucesso.
* **Monitoramento e Dashboards:** Painéis interativos para visualização de dados estatísticos e indicadores de desempenho das áreas replantadas.
* **Gestão de Usuários:** Controle de acesso para administradores e operadores de campo.

## Arquitetura e Tecnologias
Este projeto adota uma arquitetura moderna, englobando as seguintes tecnologias:
* **Backend / API REST:** Python (FastAPI)
* **Frontend:** Vue.js + **JavaScript** (para visualização de dados e gráficos)
* **Banco de Dados:** PostgreSQL
* **Infraestrutura:** Docker (para conteinerização da aplicação) e Deploy em Nuvem (Cloud).
* **Qualidade e Automação:** * Testes automatizados (Unitários e de Integração). CI/CD implementado com GitHub Actions para testes e deploy automáticos.

## Como executar o projeto localmente

### Pré-requisitos
Certifique-se de ter as seguintes ferramentas instaladas na sua máquina:
* **Git**
* **Docker** e **Docker Compose**
* **Python 3.11+** (Apenas se desejar rodar o backend fora do Docker)
* **Node.js** (Apenas se desejar rodar o frontend fora do Docker)

### Passo a Passo

**1. Clone o repositório**
```bash
git clone https://github.com/PJI110-grupo013-UNIVESP/sistema-replantio-mudas.git
cd sistema-replantio-mudas
```
**2. Configure as Variáveis de Ambiente**

Na raiz do projeto, crie um arquivo chamado `.env`. Você pode usar o modelo abaixo como referência, este arquivo guardará as credenciais do banco de dados e as chaves de segurança da API:

Você pode gerar uma `SECRET_KEY` usando o comando no terminal:
```bash
openssl rand -base64 64
```

Crie o arquivo `.env` e cole o seguinte conteúdo:
```
# Configurações do Banco de Dados PostgreSQL
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=replantio

# Configurações de Segurança do Backend (JWT)
SECRET_KEY=uma_chave_super_secreta_para_desenvolvimento
ALGORITHM=HS256

# Configuração do Primeiro Administrador do Sistema (Seeding Automático)
ADMIN_EMAIL=admin@admin.com
ADMIN_PASSWORD=SenhaAdmin123
```

**3. Inicie os serviços com o Docker**

Com o terminal aberto na raiz do projeto (onde está o arquivo docker-compose.yml), execute o comando abaixo para construir as imagens e subir os containers em segundo plano:
```
docker compose up -d --build
```

O Docker irá baixar as imagens do PostgreSQL, Node e Python, instalar as dependências e iniciar o banco de dados. O backend aguardará automaticamente até que o banco de dados esteja pronto.

### Acessando a Aplicação

Depois que os containers estiverem rodando, você pode acessar os serviços através do seu navegador:

- Frontend (Aplicação Web): http://localhost:5173
- Backend (Documentação Swagger API): http://localhost:8000/docs

### Crendências de Acesso Padrão

Ao iniciar o sistema pela primeira vez, o banco de dados será populado automaticamente com um usuário Administrador usando as credenciais definidas no seu `.env`:

- E-mail: admin@admin.com
- Senha: SenhaAdmin123

Utilize estes dados na tela de Login para entrar no Painel de Gestão e começar a utilizar o sistema.

### Comando Úteis (Docker)

- Para ver os logs da aplicação: `docker compose logs -f`
- Para desligar os serviços: `docker compose down`
- Para desligar e *apagar o banco de dados*: `docker compose down -v`