from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal, Base, engine
from ..models import GLLine
router = APIRouter(prefix="/financials", tags=["financials"])
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    rows = db.query(GLLine).all()
    totals = {}
    out_rows = []
    for r in rows:
        account = r.account or "Unknown"
        amount = float(r.amount) if r.amount is not None else 0.0
        totals[account] = totals.get(account, 0.0) + amount
        out_rows.append({"account": account, "amount": amount, "memo": r.memo})
    return {"totals": totals, "rows": out_rows}
