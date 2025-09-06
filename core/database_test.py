from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    DateTime,
    Table,
    UniqueConstraint
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    relationship,
    backref
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


class AbstractBase(Base):
    """
    Simple base abstract class model
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


enrollments = Table(
    "enrollments",
    AbstractBase.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
    UniqueConstraint("post_id", "tag_id", name="post_tag_enrolled")
)

class User(AbstractBase):
    """
    Simple user class model 
    """
    __tablename__ = "users"
    
    username = Column(String(length=50))
    email = Column(String())
    password = Column(String())
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    addresses = relationship("Address", backref="user")
    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="user")
    profile = relationship("Profile", backref="user", uselist=False)
    
    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
    

class Address(AbstractBase):
    """
    Simple Address class model
    this table has One:Many relationship with users table
    """
    __tablename__ = "addresses"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String())
    state = Column(String())
    zip_code = Column(String())
    
    def __repr__(self):
        return f"Address(id={self.id}, user_id={self.user_id}, city={self.city})"


class Profile(AbstractBase):
    """
    Simple Profile class model
    this table has One:One relationship with users table
    """
    __tablename__ = "profiles"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String())
    last_name = Column(String())
    bio = Column(Text(), nullable=True)
    
    def __repr__(self):
        return f"Profile(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


class Post(AbstractBase):
    """
    Simple Post class model
    this table has One:Many relationship with users table
    """
    __tablename__ = "posts"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String())
    content = Column(Text())
    
    comments = relationship("Comment", backref="post")
    tags = relationship("Tag", secondary=enrollments, back_populates="posts")
    
    def __repr__(self):
        return f"Post(id={self.id}, title={self.title})"
    
    
class Comment(AbstractBase):
    """
    Simple Comment class model
    this table has One:Many relationship with users, posts tables
    """
    __tablename__ = "comments"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    message = Column(Text())
    
    # parent = relationship("Comment", back_populates="children", remote_side="Comment.id")
    # children = relationship("Comment", back_populates="parent")
    children = relationship("Comment", backref=backref("parent", remote_side="Comment.id"))
    
    def __repr__(self):
        return f"Comment(id={self.id}, message={self.message})"
    
    
class Tag(AbstractBase):
    __tablename__ = "tags"
    
    name = Column(String())
    posts = relationship("Post", secondary=enrollments, back_populates="tags")
    
    def __repr__(self):
        return f"Tag(id={self.id}, name={self.name})"
    

# to create tables and database
Base.metadata.create_all(bind=engine)
