from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.database import Base
# Определение модели SQLAlchemy
class Task(Base):
    __tablename__ = 'tasks2'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
