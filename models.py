from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class OperatorModel(Base):
    __tablename__ = "operators"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    active = Column(Integer)
    max_load = Column(Integer)
    weights = Column(String)

class LeadModel(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, index=True)
    name = Column(String)

class SourceModel(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class ContactModel(Base):
    __tablename__= "contacts"
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey('leads.id'))
    source_id = Column(Integer, ForeignKey('sources.id'))
    operator_id = Column(Integer, ForeignKey('operators.id'))

