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
