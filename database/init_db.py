from database.connection import engine, Base
from database.models import UnifiedTransaction


def init_db():
    """Creates all database tables defined in ORM models."""
    try:
        print("[INFO] Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] All database tables created successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to initialize database tables: {e}")


if __name__ == "__main__":
    init_db()