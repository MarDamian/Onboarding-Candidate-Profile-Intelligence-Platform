-- Extensión pgcrypto habilitada para generar UUIDs, por si se requiere en versiones de postgreSQL < 13
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Tabla para logs de ETL
CREATE TABLE IF NOT EXISTS etl_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    records_processed INTEGER DEFAULT 0
);