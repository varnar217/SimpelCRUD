from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine(database_url):
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    return engine

def get_session(database_url):
    engine = get_engine(database_url)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal
