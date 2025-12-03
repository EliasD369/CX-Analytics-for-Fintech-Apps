# scripts/insert_data.py
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from db_config import get_db_params

# Adjust filename if needed
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_PATH = os.path.join(ROOT, "data", "processed", "cleaned_reviews.csv")

BATCH_SIZE = 1000  # adjust to memory

def connect():
    params = get_db_params()
    conn = psycopg2.connect(**params)
    return conn

def upsert_banks(conn, bank_names_map):
    """
    bank_names_map: dict mapping app tag (e.g. 'CBE') to full bank_name (optional)
    If values are simple strings, will insert bank_name=app tag and app_name=app tag.
    Returns dict: app_tag -> bank_id
    """
    result = {}
    with conn.cursor() as cur:
        for app_tag, full_name in bank_names_map.items():
            bank_name = full_name or app_tag
            # upsert banks (on bank_name unique)
            cur.execute(
                """
                INSERT INTO banks (bank_name, app_name)
                VALUES (%s, %s)
                ON CONFLICT (bank_name) DO UPDATE SET app_name = EXCLUDED.app_name
                RETURNING bank_id;
                """,
                (bank_name, app_tag)
            )
            bank_id = cur.fetchone()[0]
            result[app_tag] = bank_id
    conn.commit()
    return result

def parse_date(x):
    try:
        return pd.to_datetime(x)
    except Exception:
        return None

def prepare_rows(df, bank_id):
    # returns list of tuples matching (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
    rows = []
    for _, r in df.iterrows():
        text = r.get("clean_content") or r.get("content") or ""
        rating = int(r.get("score")) if pd.notna(r.get("score")) else None
        date_raw = r.get("at") or r.get("date") or r.get("review_date")
        review_date = parse_date(date_raw)
        sentiment_label = r.get("sentiment") or r.get("sentiment_label") or None
        sentiment_score = r.get("compound") if "compound" in r else r.get("sentiment_score") if "sentiment_score" in r else None
        source = r.get("source") if "source" in r else "Google Play"
        rows.append((
            bank_id,
            text,
            rating,
            review_date.to_pydatetime() if pd.notna(review_date) else None,
            sentiment_label,
            float(sentiment_score) if pd.notna(sentiment_score) else None,
            source
        ))
    return rows

def batch_insert_reviews(conn, rows):
    """
    rows: list of tuples as in prepare_rows
    """
    if not rows:
        return 0
    with conn.cursor() as cur:
        sql = """
            INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
            VALUES %s
            ON CONFLICT (bank_id, md5(review_text), review_date) DO NOTHING
        """
        execute_values(cur, sql, rows, page_size=1000)
    conn.commit()
    return len(rows)

def main():
    if not os.path.exists(CLEANED_PATH):
        print("Cleaned CSV not found at:", CLEANED_PATH)
        return

    df_all = pd.read_csv(CLEANED_PATH)
    print("Loaded cleaned reviews rows:", len(df_all))

    # Ensure an 'app' column exists
    if 'app' not in df_all.columns:
        raise ValueError("cleaned CSV must include 'app' column (app tag: CBE/BOA/Amole).")

    # Provide mapping app_tag -> full bank name (if you have full names)
    # Update values if needed
    bank_names_map = {
        "CBE": "Commercial Bank of Ethiopia",
        "BOA": "Bank of Abyssinia",
        "Amole": "Amole"
    }

    conn = connect()
    try:
        bank_id_map = upsert_banks(conn, bank_names_map)
        print("Bank id map:", bank_id_map)

        total_inserted = 0
        # Process per app to reduce memory usage
        for app_tag, bank_id in bank_id_map.items():
            df_app = df_all[df_all['app'] == app_tag]
            if df_app.empty:
                print(f"No rows for {app_tag}")
                continue

            # Optionally shuffle or sort by date
            rows = prepare_rows(df_app, bank_id)

            # Insert in batches
            for i in range(0, len(rows), BATCH_SIZE):
                batch = rows[i:i+BATCH_SIZE]
                inserted = batch_insert_reviews(conn, batch)
                total_inserted += inserted
                print(f"Inserted batch {i//BATCH_SIZE + 1}: {inserted} rows for {app_tag}")

        print("Total rows processed (attempted inserts):", total_inserted)
    except Exception as e:
        print("Error during insertion:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
