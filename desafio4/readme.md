# 🐳 Desafio 4: Microsserviços Independentes com Docker

Este repositório contém a solução para o Desafio 4, demonstrando a comunicação entre dois microsserviços independentes (Producer e Consumer) isolados em containers Docker e comunicando-se via HTTP.

---

## 📋 Sobre o Projeto

O objetivo é simular uma arquitetura distribuída simples composta por dois serviços:

* **Service A (User Service)**
  Fornece uma lista de usuários via API REST (JSON).

* **Service B (Report Service)**
  Consome o Service A e renderiza um relatório HTML amigável ao usuário final.

---

## 🏗️ Arquitetura e Fluxo de Dados

A comunicação é síncrona via HTTP. Ambos os serviços rodam dentro de uma **rede isolada Docker (app-network)** que oferece DNS interno.

### Diagrama

```mermaid
graph LR
    User((Usuário)) -- HTTP GET :5001/relatorio --> ServiceB[Service B\n(Consumer)]
    subgraph Docker Network
        ServiceB -- HTTP GET :5000/users --> ServiceA[Service A\n(Producer)]
        ServiceA -- JSON --> ServiceB
    end
    ServiceA -.-> DB[(Dados Mockados)]
```

---

## 🚀 Tecnologias e Decisões Técnicas

* **Python 3.9 + Flask**
  Utilizado para criar APIs simples e rápidas.

* **Docker**
  Garante isolamento total de dependências e ambiente.

* **Imagem Base: `python:3.9-slim`**
  Reduz tamanho da imagem e superfície de ataque.

* **Docker Network**
  Bridge customizada para resolução de nomes via DNS interno do Docker.

* **Requests (Service B)**
  Responsável pela comunicação HTTP com o Service A, com tratamento de exceções.

---

## 📂 Estrutura de Arquivos

```
/
├── service_a/
│   ├── app.py           # Código do microsserviço de usuários
│   ├── Dockerfile       # Instruções de build do Service A
│   └── requirements.txt # flask==3.0.0
├── service_b/
│   ├── app.py           # Código do microsserviço de relatório
│   ├── Dockerfile       # Instruções de build do Service B
│   └── requirements.txt # flask==3.0.0, requests==2.31.0
└── README.md
```

---

## 🛠️ Como Executar (Passo a Passo)

Não é necessário instalar Python localmente. Apenas Docker.

---

### **1. Criar a rede Docker**

```bash
docker network create app-network
```

---

### **2. Configurar e rodar o Serviço A (Producer)**

```bash
# Entrar na pasta
cd service_a

# Construir a imagem
docker build -t img-service-a .

# Rodar o container
docker run -d --name service-a --network app-network -p 5000:5000 img-service-a
```

Observação: O nome **service-a** deve permanecer assim para que o Service B consiga encontrá-lo via [http://service-a](http://service-a).

---

### **3. Configurar e rodar o Serviço B (Consumer)**

```bash
# Voltar para a raiz e entrar na pasta do Service B
cd ../service_b

# Construir a imagem
docker build -t img-service-b .

# Rodar o container
docker run -d --name service-b --network app-network -p 5001:5001 img-service-b
```

---

### **4. Testando a aplicação**

Acesse:

```
http://localhost:5001/relatorio
```

**Resultado esperado:**
Página HTML contendo:

* Título: *Relatório de Usuários Ativos*
* Lista com:

  * Alice Silva
  * Bob Santos
  * Carol Dias
    …cada um exibindo sua data de ativação

---

## 🔍 Endpoints Detalhados

### **Serviço A (Interno)**

```
GET http://service-a:5000/users
```

Resposta:

```json
[
  {"id": 1, "name": "Alice Silva", "active_since": "2023-01-15", "role": "Admin"},
  {"id": 2, "name": "Bob Santos", "active_since": "2022-11-02", "role": "User"},
  {"id": 3, "name": "Carol Dias", "active_since": "2023-05-20", "role": "User"}
]
```

---

### **Serviço B (Público)**

```
GET http://localhost:5001/relatorio
```

* Retorna HTML formatado.
* Em caso de falha do Service A:

  * Retorna **HTTP 503** com mensagem amigável.
  * Evita crash do serviço.

---

## 🧹 Limpeza (Como parar)

```bash
docker stop service-b service-a
docker rm service-b service-a
docker network rm app-network
```

---


