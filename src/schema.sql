DROP TABLE IF EXISTS projects;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    api_key uuid DEFAULT uuid_generate_v4 (),
    name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
