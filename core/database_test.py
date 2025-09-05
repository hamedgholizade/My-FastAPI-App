from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


SQLARCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
# SQLARCHEMY_DATABASE_URL = "sqlite:///:memory:"

# for postgres or other relational database
# SQLARCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db"
# SQLARCHEMY_DATABASE_URL = "mysql://username:password@localhost:port/db_name"

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

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=30))
    last_name = Column(String(length=30))
    
    def __repre__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"

# to create tables and database
Base.metadata.create_all(engine)
