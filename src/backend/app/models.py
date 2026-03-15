from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Credentials(Base):
    __tablename__ = "credentials"
    user = Column(String(255), nullable=False, primary_key=True)
    password = Column(String(60), nullable=False)

class Blacklist(Base):
    __tablename__ = "blacklist"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("credentials.user"), nullable=False, unique=True)
