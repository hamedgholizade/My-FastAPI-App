from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


SQLARCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

# create connector for connecting database
engine = create_engine(
    SQLARCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # Only for sqlite.db
)

# create cursor for database
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# create base class for declaring tables
Base = declarative_base()


class Person(Base):
    """
    Simple Person class model 
    """
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=255))
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"Person(id={self.id}, name={self.name})"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
