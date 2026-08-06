-- AMIP User table (not in original schema)
CREATE TABLE IF NOT EXISTS amip_user (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'viewer',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Default admin user (password: admin123)
INSERT INTO amip_user (username, password_hash, full_name, role)
VALUES ('admin', '$2b$12$DawGaSOLjkhp6JhGl4VX2umqZN2wprFEJXZ5qs9hCm3ib5uwLEKzC', 'Administrateur', 'admin')
ON CONFLICT (username) DO NOTHING;

-- Default viewer user (password: viewer123)
INSERT INTO amip_user (username, password_hash, full_name, role)
VALUES ('viewer', '$2b$12$90JwIEOITXqsItlUomPA3eYl1cV3vuy15ubR4qmxzfaU2Ni/Jq9/m', 'Observateur', 'viewer')
ON CONFLICT (username) DO NOTHING;
