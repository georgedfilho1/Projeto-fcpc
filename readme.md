# Desafios 1 ao 5

Este repositório reúne todas as soluções desenvolvidas para a série de **Desafios**, abordando conceitos fundamentais como containers, redes, volumes, microsserviços e API Gateway.  
Cada desafio possui seu próprio diretório e README detalhado.

---

## 📌 Lista de Desafios

### **Desafio 1 — Containers em Rede**
Objetivo: Demonstrar comunicação entre containers usando uma rede Docker customizada.  
Tecnologias: Nginx, Alpine + Curl, Docker Compose.  
Pontos principais:
- Rede personalizada (`bridge`)
- Servidor web acessado por container cliente
- Logs de comunicação contínua

---

### **Desafio 2 — Volumes e Persistência**
Objetivo: Demonstrar persistência de dados utilizando volumes Docker.  
Tecnologias: PostgreSQL, pgAdmin, Docker Compose.  
Pontos principais:
- Volume nomeado para armazenar dados fora do container
- Persistência após recriação do container
- Gerenciamento visual via pgAdmin

---

### **Desafio 3 — Docker Compose e Orquestração de Serviços**
Objetivo: Orquestrar múltiplos serviços interdependentes.  
Tecnologias: Flask, Redis, PostgreSQL.  
Pontos principais:
- Rede interna
- Contador persistente em Redis
- Teste de conexão com PostgreSQL
- Comunicação entre três containers

---

### **Desafio 4 — Microsserviços Independentes**
Objetivo: Simular comunicação entre microsserviços Producer/Consumer via HTTP.  
Tecnologias: Flask, Requests, Docker, Rede customizada.  
Pontos principais:
- Service A (Producer): envia JSON
- Service B (Consumer): gera relatório HTML
- Comunicação via DNS interno do Docker

---

### **Desafio 5 — API Gateway com Microsserviços**
Objetivo: Criar uma arquitetura com API Gateway centralizando o acesso a serviços.  
Tecnologias: Flask, Requests, Docker Compose.  
Pontos principais:
- Gateway como ponto único de entrada
- Integração com microsserviço de usuários e pedidos
- Orquestração via Docker Compose

---

## 📂 Estrutura Geral do Repositório

```

/
├── desafio1/   # Containers em rede
├── desafio2/   # Volumes e persistência
├── desafio3/   # Orquestração com Compose
├── desafio4/   # Microsserviços independentes
├── desafio5/   # API Gateway
└── README.md   # Este arquivo (resumo)

````

---

## 🎯 Objetivo Geral dos Projetos

Cada desafio foi projetado para fixar conhecimentos essenciais de Docker:

- Criação e execução de containers
- Redes Docker e DNS interno
- Volumes e persistência
- Comunicação entre serviços
- Estruturação de microsserviços
- Orquestração com Docker Compose
- Boas práticas de containerização

---

## 🚀 Como executar qualquer desafio

Entre na pasta correspondente e execute:

```bash
docker-compose up --build
````

Para parar:

```bash
docker-compose down
```

---

Caso deseje, posso gerar também uma **versão em inglês**, **versão minimalista**, ou **README com links diretos para cada subprojeto**.
