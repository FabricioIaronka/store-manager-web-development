DROP TABLE IF EXISTS sale_items CASCADE;
DROP TABLE IF EXISTS sales CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS clients CASCADE;
DROP TABLE IF EXISTS user_stores CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS stores CASCADE;

DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS payment_type CASCADE;

DROP FUNCTION IF EXISTS fn_update_timestamp CASCADE;

CREATE TYPE user_role AS ENUM ('seller', 'stock_manager', 'admin');

CREATE TYPE payment_type AS ENUM ('Money', 'Debit', 'Credit', 'PIX', 'Other');


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18),
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_stores (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    store_id INTEGER REFERENCES stores(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, store_id)
);

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(id),
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100),
    cpf VARCHAR(11) UNIQUE,
    number VARCHAR(20),
    email VARCHAR(255) UNIQUE
);


CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL CHECK(price >= 0),
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    category VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    client_id INTEGER REFERENCES clients(id),
    payment_type payment_type NOT NULL,
    total_value NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE sale_items (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),

    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

ALTER TABLE stores ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stores ENABLE ROW LEVEL SECURITY;
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales ENABLE ROW LEVEL SECURITY;

CREATE OR REPLACE FUNCTION fn_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_users_update
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_products_update
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION fn_update_timestamp();

DROP POLICY IF EXISTS stores_isolation_policy ON stores;
DROP POLICY IF EXISTS user_stores_isolation_policy ON user_stores;
DROP POLICY IF EXISTS tenant_isolation_policy ON clients;
DROP POLICY IF EXISTS tenant_isolation_policy ON products;
DROP POLICY IF EXISTS tenant_isolation_policy ON sales;

CREATE POLICY user_stores_isolation_policy ON user_stores
    USING (user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER)
    WITH CHECK (user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER);

CREATE POLICY stores_isolation_policy ON stores
    USING (
        owner_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER
        OR
        id IN (
            SELECT store_id FROM user_stores 
            WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER
        )
    )
    WITH CHECK (
        owner_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER
    );

CREATE POLICY tenant_isolation_policy ON clients
    USING (
        store_id IN (
            SELECT store_id FROM user_stores 
            WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER
        )
    )
    WITH CHECK (
        store_id IN (
            SELECT store_id FROM user_stores 
            WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER
        )
    );

CREATE POLICY tenant_isolation_policy ON products
    USING (store_id IN (SELECT store_id FROM user_stores WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER))
    WITH CHECK (store_id IN (SELECT store_id FROM user_stores WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER));

CREATE POLICY tenant_isolation_policy ON sales
    USING (store_id IN (SELECT store_id FROM user_stores WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER))
    WITH CHECK (store_id IN (SELECT store_id FROM user_stores WHERE user_id = NULLIF(current_setting('app.current_user_id', true), '')::INTEGER));
