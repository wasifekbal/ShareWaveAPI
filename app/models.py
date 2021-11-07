from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer,String, Boolean
from sqlalchemy import Column
from .database import Base

class Post(Base):
   __tablename__ = "posts"

   id = Column(Integer, primary_key=True, nullable=False)
   title = Column(String(100), nullable=False)
   content = Column(String(250), nullable=False)
   published = Column(Boolean, server_default='1',nullable=False)
   timestamp = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("CURRENT_TIMESTAMP"))
