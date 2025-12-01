# 🐳 Desafio 2 — Volumes e Persistência com Docker Compose

Este repositório contém a solução do **Desafio 2 — Volumes e Persistência**, cujo objetivo é demonstrar a persistência de dados de um banco PostgreSQL utilizando **volumes Docker**, mesmo após remoção e recriação de contêineres.

A solução utiliza:

- Um contêiner com **PostgreSQL 16 (alpine)** como banco de dados.
- Um contêiner com **pgAdmin 4** para administração gráfica do banco.
- Um **volume nomeado** (`dados-pg-compose`) para armazenar os dados fora do ciclo de vida do contêiner.

---

## 📌 1. Descrição da solução

A proposta deste desafio é:

1. Subir um contêiner com PostgreSQL utilizando Docker Compose.  
2. Mapear o diretório de dados do Postgres para um **volume Docker**.  
3. Comprovar que, ao remover o contêiner e recriá-lo, os dados permanecem intactos, pois estão salvos no volume.  
4. Utilizar um segundo contêiner (**pgAdmin**) para visualizar e manipular os dados de forma gráfica (opcional, mas implementado aqui).

A persistência é garantida pelo **volume nomeado** `dados-pg-compose`, que é independente do ciclo de vida do contêiner `banco`.

---

## 🏗 2. Arquitetura da solução

### 2.1 Componentes

- **Serviço `banco`**
  - Imagem: `postgres:16-alpine`
  - Banco: `meu_banco`
  - Usuário: `meuusuario`
  - Senha: `minhasenha`
  - Porta exposta: `5432:5432`
  - Volume:
    - `dados-pg-compose:/var/lib/postgresql/data`

- **Serviço `pgadmin`**
  - Imagem: `dpage/pgadmin4`
  - E-mail padrão: `admin@example.com`
  - Senha padrão: `admin`
  - Porta exposta: `8080:80`
  - Depende do serviço `banco` (`depends_on`)

- **Volume nomeado**
  - `dados-pg-compose` → mapeado em `/var/lib/postgresql/data` dentro do contêiner `banco`.

### 2.2 Diagrama 

graph LR
    User[Usuario] -->|"HTTP :8080"| PGAdmin[pgAdmin 4 web]
    User -->|"TCP :5432"| BancoHost[Host port 5432]

    subgraph DockerNetworkDefault
        PGAdmin -->|"Host=banco:5432"| Banco[PostgreSQL pg-compose]
        Banco --- Volume[Volume dados-pg-compose]
    end


---

## ⚙ 3. Decisões técnicas

1. **PostgreSQL oficial (`postgres:16-alpine`)**

   * Versão estável e leve (`alpine`), adequada para ambiente de desenvolvimento e testes de persistência.

2. **Volume nomeado (`dados-pg-compose`)**

   * Utilizado em vez de `bind mount` para:

     * Simplificar portabilidade.
     * Centralizar dados gerenciados pelo Docker.
   * Montado em `/var/lib/postgresql/data`, que é o diretório oficial de dados do Postgres.

3. **pgAdmin em contêiner separado**

   * Facilita a inspeção visual dos dados, sem necessidade de cliente SQL instalado na máquina host.
   * Acessível via navegador em `http://localhost:8080`.

4. **Docker Compose**

   * Orquestração simples dos dois serviços.
   * Gerenciamento de dependência (`depends_on`) entre `pgadmin` e `banco`.
   * Definição do volume no escopo do arquivo (`volumes: dados-pg-compose:`).

---

## 🧱 4. Arquivo `docker-compose.yml`

```yaml
version: '3.8'

services:
  banco:
    image: postgres:16-alpine
    container_name: pg-compose
    environment:
      POSTGRES_USER: meuusuario
      POSTGRES_PASSWORD: minhasenha
      POSTGRES_DB: meu_banco
    ports:
      - "5432:5432"
    volumes:
      - dados-pg-compose:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin-compose
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "8080:80"
    depends_on:
      - banco

volumes:
  dados-pg-compose:
```

---

## 🔍 5. Funcionamento detalhado (containers, volume e fluxo)

1. Ao executar `docker-compose up`, o serviço `banco` é criado com a imagem `postgres:16-alpine`.
2. O diretório interno `/var/lib/postgresql/data` é montado no volume **`dados-pg-compose`**.
3. O Postgres inicializa o banco **`meu_banco`** com usuário **`meuusuario`**.
4. O serviço `pgadmin` é iniciado e se conecta ao Postgres usando o hostname `banco` (nome do serviço no Compose) e porta `5432`.
5. Quando você cria tabelas e insere dados em `meu_banco`, esses dados são gravados no volume `dados-pg-compose`.
6. Se o contêiner `banco` for removido (por exemplo, via `docker-compose down`), o volume **permanece**.
7. Ao recriar o contêiner com `docker-compose up` (sem remover o volume), o Postgres utiliza os mesmos arquivos do volume e os dados continuam disponíveis.

---

## 🚀 6. Passo a passo: como executar

### 6.1. Pré-requisitos

* Docker instalado
* Docker Compose instalado

### 6.2. Subir os contêineres

Na pasta onde está o `docker-compose.yml`:

```bash
docker-compose up -d
```

Verificar se os contêineres estão rodando:

```bash
docker ps
```

Saída esperada (exemplo simplificado):

```bash
CONTAINER ID   IMAGE             NAMES
abcd1234       dpage/pgadmin4   pgadmin-compose
efgh5678       postgres:16-alpine   pg-compose
```

---

## 🧪 7. Testando a persistência de dados

### 7.1. Acessar o pgAdmin

1. Abra o navegador em:
   `http://localhost:8080`
2. Login:

   * E-mail: `admin@example.com`
   * Senha: `admin`

### 7.2. Configurar conexão com o Postgres

No pgAdmin:

1. Clique em **Add New Server**.
2. Aba **General**:

   * Name: `Postgres Docker`
3. Aba **Connection**:

   * Host: `banco`
   * Port: `5432`
   * Username: `meuusuario`
   * Password: `minhasenha`
4. Salve.

### 7.3. Criar uma tabela e inserir dados

No pgAdmin, abra o painel de consultas (**Query Tool**) e execute:

```sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO clientes (nome, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com');
```

Conferir os dados:

```sql
SELECT * FROM clientes;
```

Resultado esperado (exemplo):

```text
 id | nome  |       email
----+-------+--------------------
  1 | Alice | alice@example.com
  2 | Bob   | bob@example.com
```

### 7.4. Derrubar e recriar os contêineres

Derrubar os serviços (sem remover o volume):

```bash
docker-compose down
```

Os contêineres serão removidos, mas o volume `dados-pg-compose` permanecerá.

Subir novamente:

```bash
docker-compose up -d
```

Acessar novamente o pgAdmin, conectar ao mesmo servidor e executar:

```sql
SELECT * FROM clientes;
```

Se os dados aparecerem como antes, a **persistência via volume** foi comprovada.

---

## 🧹 8. Limpeza completa (incluindo volume)

Caso você queira remover **também** o volume e perder os dados:

```bash
docker-compose down -v
```

Isso irá:

* Remover os contêineres
* Remover o volume `dados-pg-compose`
* Na próxima subida (`docker-compose up`), o banco será recriado do zero.


