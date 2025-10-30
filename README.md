# Sistema de Controle de Vendas e Estoque

## 1) Problema
Pequenos e médios comerciantes frequentemente enfrentam dificuldades para controlar seu estoque e vendas de maneira organizada. Muitos ainda utilizam planilhas manuais ou anotações, o que gera inconsistências, perda de informações e falta de visibilidade sobre a saúde do negócio.  

Um sistema digital simples e acessível pode reduzir erros, melhorar a gestão do inventário e ajudar a tomar decisões mais assertivas sobre compras, promoções e fluxo de caixa.

---

## 2) Atores e Decisores
- **Usuários finais**: vendedores, atendentes e gestores de loja que utilizam o sistema diariamente para registrar vendas e atualizar o estoque.  
- **Decisores**: proprietários e gerentes, responsáveis por escolher a solução tecnológica e acompanhar relatórios de desempenho.

---

## 3) Casos de uso (de forma simples)
<!-- Formato "Ator: ações que pode fazer". -->

- **Vendedor/Atendente**: registrar vendas, consultar produtos disponíveis no estoque.  
- **Gestor de Estoque**: cadastrar novos produtos, editar informações de produtos, remover produtos, visualizar estoque baixo.  
- **Proprietário/Gerente**: acompanhar relatórios de vendas, analisar produtos mais vendidos, verificar movimentação de estoque.

---

## 4) Limites e Suposições (+ Plano B)
- O sistema será inicialmente **monousuário** e voltado para **lojas físicas pequenas**.  
- O banco de dados inicial será **SQLite** para simplicidade, podendo ser trocado por **PostgreSQL/MySQL** em cenários maiores.  
- Supondo que o usuário possua acesso a computador e internet para usar a aplicação.  
- **Plano B**: caso a aplicação web não seja viável em determinado contexto, poderá ser utilizada apenas localmente como aplicação desktop simplificada.

---

## 5) Hipóteses (valor e viabilidade) e Validação
- **Hipótese de valor**: comerciantes que atualmente usam planilhas terão ganhos de eficiência e menos erros ao migrar para este sistema.  
- **Hipótese de viabilidade**: é possível construir um MVP funcional utilizando **Python (FastAPI)** no backend e **React + Vite** no frontend em um prazo curto.  
- **Validação**: feedback com usuários reais de pequenas lojas, testes de uso em ambiente real e comparação com processos manuais.

---

## 6) Fluxo principal do usuário e primeira fatia vertical
**Fluxo principal do usuário**:  
1. Usuário acessa o sistema e faz login (quando houver autenticação).  
2. Cadastra produtos no estoque.  
3. Registra uma venda.  
4. O estoque é atualizado automaticamente.  
5. Usuário gera um relatório simples das vendas.  

**Primeira fatia vertical (MVP)**:  
- Cadastro de produtos  
- Registro de vendas  
- Atualização de estoque  

Com esse núcleo funcional já é possível entregar valor inicial e evoluir o sistema em ciclos curtos.

---

## 7) Esboços de algumas telas (Wireframes)
Para guiar o desenvolvimento da interface, foram feitos esboços de telas principais:  

- **Tela de Login**: acesso ao sistema por usuário e senha.  
- **Tela de Vendas**: registro de novas vendas, seleção de produtos e quantidade.  
- **Tela de Estoque**: listagem de produtos, status de estoque baixo e opções de adicionar/editar/remover.  

Os wireframes estão disponíveis na pasta [`/docs/wireframes`](./docs/wireframes).  

### Exemplos:
![Login](./docs/wireframes/tela_login.png)  
![Tela de Vendas](./docs/wireframes/tela_venda.png)  
![Tela de Estoque](./docs/wireframes/tela_estoque.png)
## 8) Tecnologias
<!-- Liste apenas o que você REALMENTE pretende usar agora. -->

### 8.1 Navegador
**Navegador:** React + Vite (HTML/CSS/JS)  
**Armazenamento local (se usar):** LocalStorage (sessão de usuário)  
**Hospedagem:** GitHub Pages (protótipo)  

### 8.2 Front-end (servidor de aplicação, se existir)
**Front-end (servidor):** React (SPA)  
**Hospedagem:** Vercel (possível)  

### 8.3 Back-end (API/servidor, se existir)
**Back-end (API):** FastAPI (Python)  
**Banco de dados:** SQLite (inicial, evolutivo para PostgreSQL)  
**Deploy do back-end:** Railway (possível)  

---

## 9) Plano de Dados (Dia 0) — somente itens 1–3
<!-- Defina só o essencial para criar o banco depois. -->

### 9.1 Entidades
- **Usuario** — pessoa que acessa o sistema (vendedor, gerente).  
- **Produto** — item disponível no estoque da loja.  
- **Venda** — registro de uma venda realizada, vinculada a produtos e usuários.  

---

### 9.2 Campos por entidade

#### Usuario
| Campo            | Tipo       | Obrigatório | Exemplo             |
|------------------|------------|-------------|---------------------|
| id               | número     | sim         | 1                   |
| nome             | texto      | sim         | "Ana Souza"         |
| email            | texto      | sim (único) | "ana@exemplo.com"   |
| senha_hash       | texto      | sim         | "$2a$10$..."        |
| papel            | número (0=vendedor, 1=gerente) | sim | 0 |
| dataCriacao      | data/hora  | sim         | 2025-08-20 14:30    |
| dataAtualizacao  | data/hora  | sim         | 2025-08-20 15:10    |

#### Produto
| Campo            | Tipo       | Obrigatório | Exemplo             |
|------------------|------------|-------------|---------------------|
| id               | número     | sim         | 101                 |
| nome             | texto      | sim         | "Camiseta Preta"    |
| preco            | número     | sim         | 49.90               |
| quantidade       | número     | sim         | 20                  |
| categoria        | texto      | não         | "Roupas"            |
| dataCriacao      | data/hora  | sim         | 2025-08-20 10:10    |
| dataAtualizacao  | data/hora  | sim         | 2025-08-20 12:30    |

#### Venda
| Campo            | Tipo       | Obrigatório | Exemplo             |
|------------------|------------|-------------|---------------------|
| id               | número     | sim         | 5001                |
| usuario_id       | número (fk)| sim         | 1                   |
| data             | data/hora  | sim         | 2025-08-20 14:40    |
| valor_total      | número     | sim         | 149.70              |

#### VendaProduto (tabela associativa para N:N)
| Campo            | Tipo       | Obrigatório | Exemplo             |
|------------------|------------|-------------|---------------------|
| id               | número     | sim         | 7001                |
| venda_id         | número (fk)| sim         | 5001                |
| produto_id       | número (fk)| sim         | 101                 |
| quantidade       | número     | sim         | 3                   |
| preco_unitario   | número     | sim         | 49.90               |

---

### 9.3 Relações entre entidades

* Um **Usuario** pode realizar muitas **Vendas** (1→N).  
* Uma **Venda** pertence a um **Usuario** (N→1).  
* Uma **Venda** pode ser associada a um **Cliente** (1→1, opcional).  
* Uma **Venda** pode ter muitos **Produtos** (N→N).  
* Um **Produto** pode aparecer em muitas **Vendas** (N→N).  
* A relação **ItemVenda** resolve o N→N entre **Venda** e **Produto**.

### 9.4 Modelagem (SQL)

A modelagem completa do banco de dados, incluindo a criação de tabelas, inserção de dados de exemplo e queries de teste, foi implementada e separada para melhor organização.

* **DDL QUERY**

```SQL
    \-- Criação de Tipos ENUM personalizados  
CREATE TYPE user\_role AS ENUM ('vendedor', 'gerente');  
CREATE TYPE payment\_type AS ENUM ('Money', 'Debit', 'Credit', 'PIX', 'Other');

\-- Tabela de Usuários do sistema  
CREATE TABLE users (  
    id SERIAL PRIMARY KEY,  
    name VARCHAR(255) NOT NULL,  
    email VARCHAR(255) NOT NULL UNIQUE,  
    password\_hash VARCHAR(255) NOT NULL,  
    role user\_role NOT NULL,  
    created\_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT\_TIMESTAMP,  
    updated\_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT\_TIMESTAMP  
);

\-- Tabela de Clientes da loja  
CREATE TABLE clients (  
    id SERIAL PRIMARY KEY,  
    name VARCHAR(100) NOT NULL,  
    surname VARCHAR(100),  
    cpf VARCHAR(11) UNIQUE,  
    number VARCHAR(20),  
    email VARCHAR(255) UNIQUE  
);

\-- Tabela de Produtos  
CREATE TABLE products (  
    id SERIAL PRIMARY KEY,  
    name VARCHAR(255) NOT NULL,  
    description TEXT,  
    price NUMERIC(10, 2\) NOT NULL CHECK(price \>= 0),  
    quantity INTEGER NOT NULL CHECK(quantity \>= 0),  
    category VARCHAR(100),  
    created\_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT\_TIMESTAMP,  
    updated\_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT\_TIMESTAMP  
);

\-- Tabela de Vendas  
CREATE TABLE sales (  
    id SERIAL PRIMARY KEY,  
    user\_id INTEGER NOT NULL REFERENCES users(id),  
    client\_id INTEGER REFERENCES clients(id),  
    payment\_type payment\_type NOT NULL,  
    total\_value NUMERIC(10, 2\) NOT NULL,  
    created\_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT\_TIMESTAMP  
);

\-- Tabela Associativa para os Itens de uma Venda  
CREATE TABLE sale\_items (  
    id SERIAL PRIMARY KEY,  
    sale\_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,  
    product\_id INTEGER NOT NULL REFERENCES products(id),  
    quantity INTEGER NOT NULL,  
    unit\_price NUMERIC(10, 2\) NOT NULL  
);  
```

* **DML QUERY**
```sql
    -- Inserir Usurios
INSERT INTO users (name, email, password_hash, role) VALUES
('Alice Gerente', 'alice@email.com', '$2y$10$senhahashgerente', 'gerente'),
('Bruno Vendedor', 'bruno@email.com', '$2y$10$senhahashvaluevendedor', 'vendedor');

-- Inserir Clientes
INSERT INTO clients (name, surname, cpf, number, email) VALUES
('Carlos Silva', 'de Souza', '11122233344', '49999887766', 'carlos.silva@email.com'),
('Diana Costa', 'Pereira', '55566677788', '48888776655', 'diana.costa@email.com'),
('Eduardo Lima', NULL, NULL, '47777665544', NULL);

-- Inserir Produtos
INSERT INTO products (name, description, price, quantity, category) VALUES
('Camiseta Branca', 'Camiseta de algodão Pima, cor branca', 49.90, 50, 'Vestuário'),
('Calça Jeans Slim', 'Calça jeans masculina com elastano', 119.90, 30, 'Vestuário'),
('Tênis de Corrida', 'Tênis leve para corrida, marca XPTO', 299.50, 15, 'Calçados'),
('Boné Preto', 'Boné básico com aba curva', 25.00, 40, 'Acessórios'),
('Copo Térmico', 'Copo de inox com capacidade para 500ml', 89.90, 8, 'Utilitários');

-- Inserir Venda 1 (feita por Bruno Vendedor para o cliente Carlos Silva)
INSERT INTO sales (user_id, client_id, payment_type, total_value) VALUES
(2, 1, 'Credit', 169.90);
-- Itens da Venda 1
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price) VALUES
(1, 2, 1, 119.90), -- 1 Calça Jeans
(1, 4, 2, 25.00);  -- 2 Bonés Pretos

-- Inserir Venda 2 (feita por Bruno Vendedor para o cliente Diana Costa)
INSERT INTO sales (user_id, client_id, payment_type, total_value) VALUES
(2, 2, 'PIX', 299.50);
-- Itens da Venda 2
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price) VALUES
(2, 3, 1, 299.50); -- 1 Tênis de Corrida

-- Inserir Venda 3 (feita por Alice Gerente, sem cliente identificado)
INSERT INTO sales (user_id, client_id, payment_type, total_value) VALUES
(1, NULL, 'Debit', 239.60);
-- Itens da Venda 3
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price) VALUES
(3, 1, 3, 49.90), -- 3 Camisetas Brancas
(3, 5, 1, 89.90); -- 1 Copo Térmico

```

* **DQL QUERY**

```sql
-- Query 1: Listar todos os produtos com baixo estoque (quantidade menor que 10)
SELECT
    id,
    name,
    quantity,
    category
FROM
    products
WHERE
    quantity < 10
ORDER BY
    quantity ASC;

-- Query 2: Calcular o total de vendas agrupado por dia
SELECT
    DATE(created_at) AS dia,
    SUM(total_value) AS faturamento_total,
    COUNT(id) AS numero_de_vendas
FROM
    sales
GROUP BY
    DATE(created_at)
ORDER BY
    dia DESC;


-- Query 3: Listar os 5 produtos mais vendidos (em quantidade)
SELECT
    p.id,
    p.name,
    SUM(si.quantity) AS total_vendido
FROM
    sale_items si
JOIN
    products p ON si.product_id = p.id
GROUP BY
    p.id, p.name
ORDER BY
    total_vendido DESC
LIMIT 5;


-- Query 4: Detalhar uma venda específica (ex: venda com id = 1)
SELECT
    s.id AS venda_id,
    s.created_at AS data_venda,
    p.name AS produto,
    si.quantity AS quantidade,
    si.unit_price AS preco_unitario,
    (si.quantity * si.unit_price) AS subtotal
FROM
    sales s
JOIN
    sale_items si ON s.id = si.sale_id
JOIN
    products p ON si.product_id = p.id
WHERE
    s.id = 1;


-- Query 5: Listar todas as vendas realizadas por um vendedor específico (ex: user com id = 2)
SELECT
    s.id AS venda_id,
    s.total_value AS valor_total,
    s.created_at AS data_venda,
    c.name AS nome_cliente
FROM
    sales s
LEFT JOIN
    clients c ON s.client_id = c.id
WHERE
    s.user_id = 2
ORDER BY
    s.created_at DESC;

```

### **9.5\. Dados de Teste e Endpoints da API**

### **Tabela de Endpoints**

#### **Users**

| Método | Rota | Corpo (JSON) | Resposta de Sucesso |
| :---- | :---- | :---- | :---- |
| POST | /users/ | { "name": "string", "email": "user@example.com", "password": "a\_strong\_password", "role": "seller" } | 201 Created \- Objeto do utilizador criado |
| GET | /users/ | N/A | 200 OK \- Lista de todos os utilizadores |
| GET | /users/{id} | N/A | 200 OK \- Objeto do utilizador encontrado |
| GET | /users/email/{email} | N/A | 200 OK \- Objeto do utilizador encontrado |
| PUT | /users/{id} | { "name": "new name", "role": "admin" } (campos opcionais) | 200 OK \- Objeto do utilizador atualizado |
| DELETE | /users/{id} | N/A | 204 No Content |

#### 

## 

## **10\. Tecnologias Necessárias**

* **Python 3.12.3** com **FastAPI**  
* **PostgreSQL 16**

## **11\. Como Rodar**

### **Passo a Passo**

1. Instalar Dependências:  
   Certifique-se de que tem um ambiente virtual (.venv) ativado e, de seguida, instale as dependências a partir da raiz do projeto.  
   pip install \-r requirements.txt

2. Configurar Variáveis de Ambiente:  
   Copie o ficheiro .env.example para um novo ficheiro chamado .env e preencha com as suas credenciais do banco de dados.  
   cp .env.example .env

3. Criar e Popular o Banco de Dados:  
   Certifique-se de que o seu serviço PostgreSQL está a rodar. De seguida, execute os scripts para criar a estrutura (tabelas, tipos, etc.) e popular com dados iniciais.  
   \# Exemplo de comando \- substitua com o seu utilizador e nome do banco  
   \# Executa o script para criar as tabelas  
   psql \-h localhost \-U meu\_usuario\_api \-d vendas\_db \-f src/infra/db/scripts/init.sql

   \# (Opcional) Executa o script para popular com dados  
   psql \-h localhost \-U meu\_usuario\_api \-d vendas\_db \-f src/infra/db/scripts/dml.sql

### **Comandos de Execução**

* **Modo de Desenvolvimento (com auto-reload):**  
  uvicorn src.main:app \--reload \--log-level debug

* **Modo de Produção:**  
  uvicorn src.main:app \--host 0.0.0.0 \--port 8000

### **Porta Padrão**

* **8000**

## **12\. Variáveis de Ambiente**

As seguintes variáveis de ambiente são necessárias para a conexão com o banco de dados. Elas devem ser definidas num ficheiro .env na raiz do projeto.

* DB\_HOST: O endereço do servidor do banco de dados (ex: localhost).  
* DB\_PORT: A porta do servidor do banco de dados (ex: 5432).  
* DB\_USER: O nome de utilizador para a conexão.  
* DB\_PASSWORD: A senha para o utilizador especificado.  
* DB\_NAME: O nome do banco de dados ao qual se conectar.

#### **.env.example**

DB\_HOST=localhost  
DB\_PORT=5432  
DB\_USER=  
DB\_PASSWORD=  
DB\_NAME=

#### 
