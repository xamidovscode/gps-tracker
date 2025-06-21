from sqlalchemy import create_engine

DATABASE_URL = "postgresql://test:test@localhost/test"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # sqlite-specific

