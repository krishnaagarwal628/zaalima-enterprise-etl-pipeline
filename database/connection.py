import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Default to SQLite local database for development if no POSTGRES_URL is provided
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data_lake/zaalima_warehouse.db")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print(f"[SUCCESS] Connected to Database successfully via SQLAlchemy!")
            print(f"[INFO] Engine target: {engine.url}")
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")