-- Initial schema for Gravitas Chat History
CREATE TABLE IF NOT EXISTS history (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_history_timestamp ON history(timestamp);
