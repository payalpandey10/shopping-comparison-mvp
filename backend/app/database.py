"""
database.py
------------
This file's ONLY job is to connect our Python code to Postgres.
Everything else in the app imports `engine` or `get_db` from here.

We use SQLAlchemy, which lets us work with Python classes (see models.py)
instead of writing raw SQL for every query.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This actually reads the .env file and loads its contents so
# os.getenv() below can see them. Without this line, .env is
# never read and we silently fall back to the placeholder default.
load_dotenv()

# The database connection string comes from your .env file.
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/shopping_comparison"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our table models (in models.py) will inherit from this Base class.
Base = declarative_base()


def get_db():
    """
    This function gives each API request its own database session,
    and makes sure it's closed properly afterward.
    FastAPI will call this automatically wherever we need DB access.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()