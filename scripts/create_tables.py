# scripts/create_tables.py
import psycopg2
from psycopg2 import sql
from db_config import get_db_params

DDL = """
-- Banks table
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name TEXT NOT NULL UNIQUE,
    app_name TEXT NOT NULL
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    review_hash CHAR(32) GENERATED ALWAYS AS (md5(review_text)) STORED,
    rating SMALLINT,
    review_date TIMESTAMP,
    sentiment_label TEXT,
    sentiment_score FLOAT,
    source TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (bank_id, review_hash, review_date)
);
"""

def main():
    params = get_db_params()
    conn = None
    try:
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(DDL)
            print("Tables created/verified successfully.")
    except Exception as e:
        print("Error creating tables:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
