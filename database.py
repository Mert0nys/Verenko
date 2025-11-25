from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///crm.db"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, bind=engine)