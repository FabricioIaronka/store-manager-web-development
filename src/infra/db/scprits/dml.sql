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
