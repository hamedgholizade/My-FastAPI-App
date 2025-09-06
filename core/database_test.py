from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean
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
    last_name = Column(String(length=30), nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"

# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

# Inserting adata(create)
# hamed = User(first_name="mohsen", last_name="golriz", age=34)
# session.add(hamed)
# session.commit()

# bulk insert(bulk_create)
# mohsen = User(first_name="mohsen", last_name="golriz", age=34)
# zahra = User(first_name="zahra", last_name="fadai", age=23)
# session.add_all([mohsen, zahra])
# session.commit()

# retrieve all data(get-list)
# users = session.query(User).all()
# print(type(users), users)
# print([user.age for user in users])

# retrieve data(get-detail)
# user = session.query(User).filter_by(first_name="hamed").first()
# print(user, type(user))

# updating a record of data(PUT/PATCH)
# user.last_name = "gholizade"
# session.commit()

# delete a record of data(DELETE)
# if user:
#     session.delete(user)
#     session.commit()
# else:
#     print("user does not exist")
