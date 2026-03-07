from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Credentials(Base):
    __tablename__ = "credentials"
    user = Column(String(255), nullable=False, primary_key=True)
    password = Column(String(60), nullable=False)
