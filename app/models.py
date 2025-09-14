from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
import enum
class DocType(str, enum.Enum):
    pnl = "pnl"
    rent_roll = "rent_roll"
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    source_url = Column(String, nullable=True)
    storage_key = Column(String, nullable=False, unique=True)
    checksum = Column(String, nullable=False)
    doc_type = Column(Enum(DocType), nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="stored")
    message = Column(String, nullable=True)
class Period(Base):
    __tablename__ = "periods"
    id = Column(Integer, primary_key=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    __table_args__ = (UniqueConstraint("year","month", name="uq_period"), )
class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    address = Column(String, nullable=True)
class GLLine(Base):
    __tablename__ = "gl_lines"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))
    period_id = Column(Integer, ForeignKey("periods.id"))
    account = Column(String, index=True)
    amount = Column(Numeric(14,2))
    memo = Column(String)
