# scripts/db_config.py
import os
from dotenv import load_dotenv

# Load .env from project root (if present)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(ROOT, ".env")
load_dotenv(dotenv_path)

def get_db_params():
    """Return a dict with connection params for psycopg2.connect(**params)."""
    params = {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", 5432)),
        "dbname": os.getenv("PG_DATABASE", "bank_reviews"),
        "user": os.getenv("PG_USER", "postgres"),
        "password": os.getenv("PG_PASSWORD", ""),
    }
    return params
