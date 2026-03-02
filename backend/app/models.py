from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GeneratedCode(Base):
    __tablename__ = "generated_codes"
    code = Column(String(16), primary_key=True, nullable=False)
