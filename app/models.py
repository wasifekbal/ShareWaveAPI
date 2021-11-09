from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer, String, Boolean
from sqlalchemy import Column
from .database import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(name="users_posts_fk",
                     column="users.id", ondelete="cascade"), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(250), nullable=False)
    published = Column(Boolean, server_default='1', nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False,
                       server_default=text("CURRENT_TIMESTAMP"))


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    last_modified = Column(TIMESTAMP(
        timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
