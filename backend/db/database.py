from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import Settings # <-- Import the Class (Capital S)

# 1. Instantiate Settings() to get the URL
DATABASE_URL = Settings().DATABASE_URL

# 2. Optimized Engine for PostgreSQL
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,
    pool_size=10, 
    max_overflow=20
)

# Create the SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modern way to declare Base 
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper to create tables
def create_tables():
    Base.metadata.create_all(bind=engine)