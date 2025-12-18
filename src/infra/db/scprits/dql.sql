-- Query 1: Listar produtos com baixo estoque APENAS da Loja 1 (Matriz)
SELECT 
    id, name, quantity, price 
FROM 
    products 
WHERE 
    store_id = 1 
    AND quantity < 15;

-- Query 2: Relatório de Vendas consolidadas POR LOJA
-- Útil para o Admin ver qual loja está faturando mais
SELECT 
    st.name AS nome_loja,
    COUNT(s.id) AS qtd_vendas,
    SUM(s.total_value) AS faturamento_total
FROM 
    sales s
JOIN 
    stores st ON s.store_id = st.id
GROUP BY 
    st.name
ORDER BY 
    faturamento_total DESC;

-- Query 3: Ver quais usuários têm acesso a quais lojas
-- (Isso ajuda a debugar problemas de permissão)
SELECT 
    u.name AS usuario,
    u.role AS cargo,
    s.name AS loja_permitida
FROM 
    users u
JOIN 
    user_stores us ON u.id = us.user_id
JOIN 
    stores s ON us.store_id = s.id
ORDER BY 
    u.name;

-- Query 4: Detalhes de uma venda (Nota Fiscal simples)
-- Mostra: Loja, Vendedor, Cliente, Produtos e Total
SELECT 
    st.name AS loja,
    u.name AS vendedor,
    c.name AS cliente,
    p.name AS produto,
    si.quantity AS qtd,
    si.unit_price AS preco_unit,
    (si.quantity * si.unit_price) AS subtotal
FROM 
    sale_items si
JOIN sales s ON si.sale_id = s.id
JOIN products p ON si.product_id = p.id
JOIN stores st ON s.store_id = st.id
JOIN users u ON s.user_id = u.id
LEFT JOIN clients c ON s.client_id = c.id
WHERE 
    s.id = 1; -- Filtra pela Venda ID 1