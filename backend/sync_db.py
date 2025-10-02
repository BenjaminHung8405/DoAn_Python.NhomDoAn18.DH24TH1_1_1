"""
Small helper to synchronize SQLAlchemy models to the database.

Usage:
  python sync_db.py

This will load DATABASE_URL from the environment (or .env) and run
models.Base.metadata.create_all(bind=engine).

Note: For production use Alembic migrations. This script is intended for
development or quick syncing.
"""
import os
from dotenv import load_dotenv

load_dotenv()

from app import models
from app.database import engine
from sqlalchemy import text


def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL not set in environment (.env). Aborting.")
        return
    print(f"Connecting to {database_url}")
    print("Creating/updating tables from models...")
    # Ensure we use the 'public' schema (Neon sometimes requires explicit search_path)
    with engine.connect() as conn:
        try:
            # ensure public schema exists and set search path
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
            conn.execute(text("SET search_path TO public"))
            conn.commit()
        except Exception:
            # if SET fails, ignore and proceed — DB may default to public
            pass
        # Use the same connection for create_all so the search_path applies
        models.Base.metadata.create_all(bind=conn)
    print("Done. Tables created/updated.")


if __name__ == "__main__":
    main()
