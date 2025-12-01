# 🐳 Desafio 1 — Containers em Rede (Docker Networking)

Este projeto implementa o **Desafio 1 — Containers em Rede**, cujo objetivo é demonstrar a comunicação entre dois containers Docker conectados a uma **rede customizada**.  
A solução utiliza:

- **Nginx** como servidor web (container servidor)
- **Alpine Linux + Curl** como cliente que realiza requisições periódicas
- **Docker Compose** para orquestração
- **Rede customizada bridge** para comunicação interna

---

# 📌 1. Descrição da solução

O desafio consiste em criar **dois containers** que se comunicam entre si utilizando uma **rede Docker nomeada**.  
No sistema implementado:

- O **container servidor** executa um servidor Nginx na porta **8080 do host** (mapeada para **80 do container**).
- O **container cliente** executa um script em loop infinito que:
  1. Usa `curl` para enviar requisições HTTP ao servidor.
  2. Exibe no console a resposta recebida.
  3. Aguarda 5 segundos e repete o ciclo.

A comunicação entre os containers é feita usando o **hostname do serviço**:  
```

[http://servidor](http://servidor)

````

A rede personalizada permite que os containers se descubram automaticamente via DNS interno do Docker.

---

# 🏗 2. Arquitetura da solução

## 2.1 Visão geral

flowchart LR
    Cliente[Container cliente curl loop] -->|"HTTP GET"| Servidor[Container servidor Nginx]

    subgraph RedeDockerCustomizada
        Servidor
        Cliente
    end

## 2.2 Componentes

| Componente | Imagem        | Função                                      | Porta                    |
| ---------- | ------------- | ------------------------------------------- | ------------------------ |
| Servidor   | nginx         | Processa requisições HTTP                   | Host:8080 → Container:80 |
| Cliente    | alpine + curl | Envia requisições repetidamente ao servidor | Não exposta              |

## 2.3 Rede Docker

* Nome: **`minha-rede-customizada`**
* Driver: **bridge**
* Função: permitir comunicação direta entre containers pelo nome do serviço
  Via DNS interno do Docker:

```
curl http://servidor
```

---

# ⚙ 3. Decisões técnicas

### 3.1 Uso do Nginx como servidor web

Motivo:

* Leve, rápido e não requer configuração adicional.
* Responde com página HTML padrão, suficiente para demonstração da comunicação.

### 3.2 Cliente baseado em Alpine Linux

* Extremamente leve.
* Permite instalação mínima via:

  ```
  apk add --no-cache curl
  ```

### 3.3 Loop infinito com Curl

* Demonstra tráfego contínuo entre os containers.
* Simplifica a visualização dos logs de comunicação.

### 3.4 Rede bridge customizada

Motivo:

* Isola os containers do resto do sistema.
* Permite DNS interno para que serviços se encontrem pelo nome.

---

# 📂 4. Arquivo `docker-compose.yml`

```yaml
version: '3.8'

services:
  # Container 1: O Servidor
  servidor:
    image: nginx
    container_name: servidor-web
    ports:
      - "8080:80"
    networks:
      - minha-rede-customizada

  # Container 2: O Cliente
  cliente:
    image: alpine
    container_name: cliente-curl
    # Instala curl e roda o loop infinito
    command: >
      /bin/sh -c "apk add --no-cache curl &&
      while true; do
        echo '--- Solicitando ao servidor ---';
        curl http://servidor;
        sleep 5;
      done"
    depends_on:
      - servidor
    networks:
      - minha-rede-customizada

# Definição da Rede
networks:
  minha-rede-customizada:
    driver: bridge
```

---

# 🔍 5. Explicação detalhada do funcionamento

### 5.1 Inicialização

Ao executar `docker-compose up`, o Docker:

1. Cria a rede **minha-rede-customizada**.
2. Sobe o container **servidor** usando Nginx.
3. Sobe o container **cliente**, que:

   * Instala `curl`.
   * Inicia um loop `while true`.

### 5.2 Comunicação interna

* O cliente envia requisições para:

```
http://servidor
```

* O Docker resolve o nome **servidor** usando seu DNS interno.
* A requisição chega ao container Nginx.
* O servidor responde com a página padrão do Nginx.

### 5.3 Logs de comunicação

O cliente imprime a cada 5 segundos:

```
--- Solicitando ao servidor ---
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

Isso comprova:

* A rede está funcionando.
* O container cliente alcança o servidor.
* O servidor responde corretamente.

---

# 🚀 6. Instruções de execução

## 6.1 Subir os containers

```bash
docker-compose up
```

Ou em segundo plano:

```bash
docker-compose up -d
```

## 6.2 Ver logs da comunicação

```bash
docker logs -f cliente-curl
```

Saída esperada:

```
--- Solicitando ao servidor ---
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

## 6.3 Testar o servidor diretamente pelo navegador (opcional)

Acessar:

```
http://localhost:8080
```

---

# 🧪 7. Evidência de comunicação funcional

Trecho real dos logs do cliente:

```
--- Solicitando ao servidor ---
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
</head>
<body>
<h1>Welcome to nginx!</h1>
</body>
</html>
```

Resumo do comportamento:

* O cliente consegue resolver DNS para `servidor`
* A requisição HTTP completa é bem-sucedida
* A rede customizada está funcionando

---

# 🧹 8. Encerrando e limpando tudo

Para parar e remover containers:

```bash
docker-compose down
```

Para destruir a rede também:

```bash
docker network rm minha-rede-customizada
```

---
