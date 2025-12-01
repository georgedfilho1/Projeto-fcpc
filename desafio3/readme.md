# 🐳 Desafio 3 — Docker Compose: Orquestração de Serviços

Este projeto consiste em uma aplicação web desenvolvida em Python (Flask) que orquestra três serviços dependentes utilizando Docker Compose. O objetivo é demonstrar comunicação entre contêineres, persistência de dados e boas práticas de configuração de ambiente.

---

## 🏗️ Arquitetura da Solução

A aplicação segue uma arquitetura de microsserviços simplificada, onde cada responsabilidade é isolada em seu próprio contêiner.

### **Diagrama de Comunicação**

```mermaid
graph TD
    User((User / Browser)) -->|Porta 5000:5000| Web[Serviço: WEB (Flask)]
    Web -->|Lê/Escreve| Cache[Serviço: CACHE (Redis)]
    Web -->|Verifica Conexão| DB[Serviço: DB (PostgreSQL)]
    
    subgraph "Docker Network: minha-rede-interna"
        Web
        Cache
        DB
    end

    style Web fill:#f9f,stroke:#333,stroke-width:2px
    style Cache fill:#ff9,stroke:#333,stroke-width:2px
    style DB fill:#9cf,stroke:#333,stroke-width:2px
```

---

## 📦 Componentes

| Serviço | Tecnologia        | Responsabilidade                                                |
| ------- | ----------------- | --------------------------------------------------------------- |
| Web     | Python (Flask)    | Recebe requisições HTTP, conecta ao Redis e valida o PostgreSQL |
| Cache   | Redis (Alpine)    | Armazena contador em memória                                    |
| DB      | PostgreSQL Alpine | Persistência de dados via volume                                |

---

## ⚙️ Decisões Técnicas e Boas Práticas

### **1. Rede Interna: `minha-rede-interna`**

**Motivo:** Isola os serviços e permite comunicação via hostname dos contêineres graças ao DNS interno do Docker.

### **2. Variáveis de Ambiente**

**Motivo:** Segue o padrão *12-Factor App*, evitando credenciais hardcoded.

### **3. Orquestração com `depends_on`**

**Motivo:** Garante a inicialização do banco e do Redis antes da aplicação Flask.

### **4. Imagens Otimizadas (Alpine / Slim)**

**Motivo:** Reduz tamanho final e melhora segurança.

---

## 🚀 Como Executar o Projeto

### **Pré-requisitos**

* Docker
* Docker Compose

### **Passo a Passo**

Clone ou baixe os arquivos do projeto.

Suba os serviços:

```bash
docker-compose up --build
```

Acesse a aplicação:

```
http://localhost:5000
```

---

## ✅ Como Testar (Validação)

### **1. Teste do Cache (Redis)**

Recarregue a página. O contador deve incrementar.

### **2. Teste do Banco (PostgreSQL)**

A página deve exibir:

```
Database (Postgres): Conectado ao PostgreSQL com sucesso!
```

### **3. Teste de Persistência**

Execute:

```bash
docker-compose down
docker-compose up
```

O banco persiste; o Redis reinicia o contador.

---

## 📂 Estrutura de Arquivos

```
├── app.py                
├── docker-compose.yml   
├── Dockerfile          
├── README.md            
└── requirements.txt      
```

---
