CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    "name" TEXT,
    "limit" BIGINT,
    balance BIGINT
);

CREATE TABLE "transaction" (
    id SERIAL PRIMARY KEY,
    "value" BIGINT,
    "type" CHAR(1),
    "description" TEXT,
    created_at TIMESTAMPTZ,
    customer_id INTEGER REFERENCES customer(id)
);

DO $$
BEGIN
  INSERT INTO customer (id, "name", "limit", balance)
  VALUES 
      (1, 'João Silva', 100000, 0),
      (2, 'Maria Santos', 80000, 0),
      (3, 'Pedro Oliveira', 1000000, 0),
      (4, 'Ana Costa', 10000000, 0),
      (5, 'Carlos Rodrigues', 500000, 0);
END; $$
