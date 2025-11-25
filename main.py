from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Base, OperatorModel, SourceModel, LeadModel, ContactModel
from database import engine, SessionLocal
from schemas import OperatorCreate, Operator, SourceSchema, Lead, ContactSchema


Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/operators/", response_model=Operator)
def create_operators(operator: OperatorCreate, db: Session = Depends(get_db)):
    operator_db = OperatorModel(**operator.dict())
    db.add(operator_db)
    db.commit()
    db.refresh(operator_db)
    return operator_db

@app.get("/operators", response_model=List[Operator])
def get_operators(db: Session = Depends(get_db)):
    return db.query(OperatorModel).all()

@app.patch("/operators/{operator_id}", response_model=Operator)
def update_operator(operator_id: int, operator: OperatorCreate, db: Session = Depends(get_db)):
    db_operator = db.query(OperatorModel).filter(OperatorModel.id == operator_id).first()
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    
    for key, value in operator.dict().items():
        setattr(db_operator, key, value)

    db.commit()
    return db_operator

@app.post("/sources", response_model=SourceSchema)
def create_source(source: SourceSchema, db: Session = Depends(get_db)):
    source_db = SourceModel(**source.dict())
    db.add(source_db)
    db.commit()
    db.refresh(source_db)
    return source_db

@app.patch("/sources/{source_id}/operators")
def set_operators_for_source(source_id: int, operators: List[int], db: Session = Depends(get_db)):
    source = db.query(SourceModel).filter(SourceModel.id == source_id).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")

    db.commit()
    return {"message": f"Operators updated for source {source.name}"}

@app.post("/contacts", response_model=ContactSchema)
def create_contact(external_id: str, source_id: int, db: Session = Depends(get_db)):
    lead = db.query(LeadModel).filter(LeadModel.external_id == external_id).first()
    
    if lead is None:
        lead = LeadModel(external_id=external_id, name="Unnamed Lead")
        db.add(lead)
        db.commit()

    source = db.query(SourceModel).filter(SourceModel.id == source_id).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")

    available_operators = db.query(OperatorModel).filter(OperatorModel.active == 1).all()
    
    if not available_operators:
        raise HTTPException(status_code=400, detail="No available operators")

    selected_operator = available_operators[0]
    contact = ContactModel(lead_id=lead.id, source_id=source.id, operator_id=selected_operator.id)
    db.add(contact)
    db.commit()
    db.refresh(contact) 

    return {
        "id": contact.id, 
        "lead_id": contact.lead_id,
        "source_id": contact.source_id,
        "operator_id": contact.operator_id
    }

@app.get("/leads", response_model=List[Lead])
def get_leads(db: Session = Depends(get_db)):
    return db.query(LeadModel).all()

@app.get("/distribution")
def get_distribution(db: Session = Depends(get_db)):
    contacts = db.query(ContactModel).all()
    operator_distribution = {}
    for contact in contacts:
        operator_distribution.setdefault(contact.operator_id, []).append(contact)
    return operator_distribution
