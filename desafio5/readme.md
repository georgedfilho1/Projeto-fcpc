
# 🐳 **Desafio 5 — Microsserviços com API Gateway**

Este projeto implementa uma arquitetura de microsserviços integrada por um **API Gateway** responsável por centralizar chamadas para dois serviços independentes:

* **Microsserviço de Usuários**
* **Microsserviço de Pedidos**

Os três serviços rodam de forma isolada em contêineres Docker, organizados através de um arquivo `docker-compose.yml`.

---

# 📌 **1. Descrição da Solução**

A solução simula uma arquitetura real de microsserviços em que o **API Gateway** funciona como **ponto único de entrada**, expondo dois endpoints públicos:

* `/users` → Encaminha requisição ao microsserviço de usuários
* `/orders` → Encaminha requisição ao microsserviço de pedidos

Internamente, o Gateway se comunica com os demais serviços usando **requisições HTTP internas na rede Docker**, garantindo isolamento e evitando exposição desnecessária de portas.

O objetivo é demonstrar:

* Orquestração com Docker Compose
* Resolução de nomes via DNS interno
* Isolamento de serviços
* Centralização de tráfego via Gateway
* Tratamento de falhas (timeouts, erro 503, etc.)

---

# 🏗️ **2. Arquitetura da Solução**

A comunicação ocorre da seguinte forma:

1. O usuário acessa **[http://localhost:4000](http://localhost:4000)**
2. O API Gateway recebe e roteia as requisições
3. O Gateway chama os microsserviços internos pela rede
4. Os serviços de usuários e pedidos devolvem JSON ao Gateway

---

## **Diagrama de Arquitetura**

```mermaid
graph TD
    User((Cliente)) -->|HTTP :4000| Gateway[API Gateway\nporta interna 8080]
    
    subgraph Docker Network: "minha-rede"
        Gateway -->|GET /users| UsersService[Users Service\nporta interna 5000]
        Gateway -->|GET /orders| OrdersService[Orders Service\nporta interna 5000]
    end
```

---

## **Microsserviços**

| Serviço        | Papel                                    | Porta Interna | Exposta?      | Container         |
| -------------- | ---------------------------------------- | ------------- | ------------- | ----------------- |
| Users Service  | Envia lista de usuários                  | 5000          | Não           | users_container   |
| Orders Service | Envia lista de pedidos                   | 5000          | Não           | orders_container  |
| API Gateway    | Único acesso externo, roteia requisições | 8080          | **Sim: 4000** | gateway_container |

---

# ⚙️ **3. Decisões Técnicas**

### **a) API Gateway como Single Point of Entry (SPOE)**

Centraliza acesso, abstrai complexidade interna e permite escalabilidade independente dos microsserviços.

### **b) Comunicação via HTTP interna**

Os serviços não expõem portas ao host; apenas o gateway fica acessível.

### **c) Docker Compose para orquestração**

Gerencia:

* Build das imagens
* Ordem de inicialização (`depends_on`)
* Rede interna
* Nomes de containers fixos (resolução DNS)

### **d) Network bridge customizada (`minha-rede`)**

Motivos:

* Isolamento dos serviços
* Comunicação simplificada usando nomes dos containers
* Segurança (evita exposição desnecessária)

### **e) Uso de imagens base `python:3.9-slim`**

Motivos:

* Imagens leves
* Menor superfície de ataque
* Build mais rápido

### **f) Tratamento de erros no Gateway**

Em caso de falha na chamada interna, o Gateway retorna:

```json
{ "error": "Service Users unavailable" }
```

ou

```json
{ "error": "Service Orders unavailable" }
```

com status **503 Service Unavailable**.

---

# 📂 **4. Estrutura do Projeto**

```
/
├── gateway/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── service-users/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── service-orders/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── docker-compose.yml
```

---

# 🔍 **5. Explicação Completa dos Componentes**

## **Gateway**

* Porta interna: **8080**
* Porta exposta no host: **4000**
* Rotas:

  * `/users`
  * `/orders`

Usa a biblioteca **requests** para chamar serviços internos.

---

## **Users Service**

Retorna:

```json
[
  {"id": 1, "name": "Alice", "email": "alice@exemplo.com"},
  {"id": 2, "name": "Bob", "email": "bob@exemplo.com"}
]
```

---

## **Orders Service**

Retorna:

```json
[
  {"id": 101, "item": "Notebook", "price": 2500, "user_id": 1},
  {"id": 102, "item": "Mouse", "price": 50, "user_id": 1}
]
```

---

## **Rede Docker**

Todos os serviços utilizam a mesma rede:

```yaml
networks:
  minha-rede:
    driver: bridge
```

A comunicação ocorre pelos nomes:

* `http://users_service:5000/users`
* `http://orders_service:5000/orders`

---

# 🚀 **6. Como Executar o Projeto**

## **Pré-requisitos**

* Docker instalado
* Docker Compose instalado

---

## **Passo 1 — Clonar o projeto**

```bash
git clone <seu-repositorio>
cd desafio5
```

---

## **Passo 2 — Subir todos os serviços**

```bash
docker-compose up --build
```

Aguarde a mensagem:

```
API Gateway rodando!
```

---

# 🧪 **7. Como Testar a Aplicação**

Abra no navegador ou use curl/Postman:

### **1. Testar status do gateway**

```
http://localhost:4000/
```

### **2. Obter usuários**

```
http://localhost:4000/users
```

### **3. Obter pedidos**

```
http://localhost:4000/orders
```

### **Resultado esperado**

O Gateway devolverá o JSON proveniente dos serviços internos.

---

# 🧹 **8. Como Encerrar e Remover os Contêineres**

```bash
docker-compose down
```

Caso queira limpar tudo:

```bash
docker rm -f users_container orders_container gateway_container
docker network rm minha-rede
```

