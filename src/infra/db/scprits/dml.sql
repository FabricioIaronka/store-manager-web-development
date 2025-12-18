-- --- LIMPEZA DE DADOS (Opcional, para evitar duplicados) ---
TRUNCATE TABLE sale_items, sales, products, clients, user_stores, stores, users RESTART IDENTITY CASCADE;

-- 1. INSERIR UTILIZADORES
-- Senha para ambos é 'secret': $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
INSERT INTO users (name, email, password_hash, role) VALUES
('Alice Proprietária', 'alice@email.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin'),
('Bruno Vendedor', 'bruno@email.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'seller');

-- 2. INSERIR LOJAS
-- Alice (ID 1) é a dona de ambas as lojas
INSERT INTO stores (name, cnpj, owner_id) VALUES
('Loja Matriz - Eletrônicos', '12.345.678/0001-99', 1),
('Filial Centro - Roupas', '98.765.432/0001-11', 1);

-- 3. VINCULAR UTILIZADORES ÀS LOJAS (Tabela Associativa)
INSERT INTO user_stores (user_id, store_id) VALUES
(1, 1), -- Alice trabalha na Loja 1
(1, 2), -- Alice trabalha na Loja 2
(2, 1); -- Bruno trabalha APENAS na Loja 1

-- 4. INSERIR CLIENTES (Segregados por Loja)
INSERT INTO clients (store_id, name, surname, cpf, number, email) VALUES
-- Clientes da Loja 1 (Eletrônicos)
(1, 'Carlos Silva', 'Almeida', '11122233344', '11999990000', 'carlos@loja1.com'),
(1, 'Diana Prince', 'Amazonas', '22233344455', '11988887777', 'diana@loja1.com'),
-- Clientes da Loja 2 (Roupas) - Note que o CPF pode até repetir se fosse outra pessoa em outra loja
(2, 'Eduardo Stark', 'Winterfell', '33344455566', '21999991111', 'eduardo@loja2.com');

-- 5. INSERIR PRODUTOS (Estoque isolado por loja)
INSERT INTO products (store_id, name, description, price, quantity, category) VALUES
-- Loja 1: Eletrônicos
(1, 'Notebook Gamer', 'i7, 16GB RAM, RTX 3060', 4500.00, 10, 'Computadores'),
(1, 'Mouse Sem Fio', 'Mouse ergonômico 2.4Ghz', 150.00, 50, 'Periféricos'),
(1, 'Teclado Mecânico', 'Switch Blue RGB', 300.00, 20, 'Periféricos'),
-- Loja 2: Roupas
(2, 'Camiseta Básica', 'Algodão Pima', 49.90, 100, 'Vestuário'),
(2, 'Calça Jeans', 'Slim Fit Azul', 120.00, 40, 'Vestuário');

-- 6. INSERIR VENDAS
-- Venda 1: Feita na Loja 1, pelo Bruno (User 2), para o Carlos (Client 1)
INSERT INTO sales (store_id, user_id, client_id, payment_type, total_value) VALUES
(1, 2, 1, 'Credit', 4650.00);

-- Itens da Venda 1
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 4500.00), -- 1 Notebook
(1, 2, 1, 150.00);  -- 1 Mouse

-- Venda 2: Feita na Loja 2, pela Alice (User 1), para o Eduardo (Client 3)
INSERT INTO sales (store_id, user_id, client_id, payment_type, total_value) VALUES
(2, 1, 3, 'PIX', 99.80);

-- Itens da Venda 2
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price) VALUES
(2, 4, 2, 49.90); -- 2 Camisetas