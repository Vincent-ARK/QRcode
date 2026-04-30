import os
import sys

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from sqlalchemy.orm import Session
import uvicorn

# When running `python app/main.py` from backend/, ensure the package root is on sys.path.
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from . import crud, models, schemas
    from .database import SessionLocal, engine
except ImportError:
    from app import crud, models, schemas
    from app.database import SessionLocal, engine

import qrcode
import io
from datetime import datetime
import validators

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dynamic QR Code System")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_url(url: str) -> bool:
    if not validators.url(url):
        return False
    # Add more checks for malicious URLs if needed
    return True

@app.get("/")
def root():
    return {"status": "ok", "message": "Dynamic QR Code System is running", "docs": "/docs"}

@app.post("/qr", response_model=schemas.QRCode)
def create_qr_code(qr_code: schemas.QRCodeCreate, db: Session = Depends(get_db)):
    if not validate_url(str(qr_code.original_url)):
        raise HTTPException(status_code=400, detail="Invalid URL")
    return crud.create_qr_code(db=db, qr_code=qr_code)

@app.get("/qr/{token:path}/image")
def get_qr_image(token: str, request: Request, db: Session = Depends(get_db)):
    db_qr = crud.get_qr_code_by_token(db, token)
    if not db_qr:
        raise HTTPException(status_code=404, detail="QR code not found")
    if db_qr.expires_at and datetime.utcnow() > db_qr.expires_at:
        raise HTTPException(status_code=410, detail="QR code expired")
    
    short_url = request.url_for("redirect_qr_code", token=token)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(short_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/png")

@app.get("/qr/{token:path}")
def redirect_qr_code(token: str, db: Session = Depends(get_db)):
    db_qr = crud.get_qr_code_by_token(db, token)
    if not db_qr:
        raise HTTPException(status_code=404, detail="QR code not found")
    if db_qr.expires_at and datetime.utcnow() > db_qr.expires_at:
        raise HTTPException(status_code=410, detail="QR code expired")
    return RedirectResponse(url=db_qr.original_url, status_code=302)

@app.put("/qr/{token:path}", response_model=schemas.QRCode)
def update_qr_code(token: str, qr_code_update: schemas.QRCodeUpdate, db: Session = Depends(get_db)):
    if qr_code_update.original_url and not validate_url(str(qr_code_update.original_url)):
        raise HTTPException(status_code=400, detail="Invalid URL")
    db_qr = crud.update_qr_code(db, token, qr_code_update)
    if not db_qr:
        raise HTTPException(status_code=404, detail="QR code not found")
    return db_qr

@app.delete("/qr/{token:path}")
def delete_qr_code(token: str, db: Session = Depends(get_db)):
    db_qr = crud.delete_qr_code(db, token)
    if not db_qr:
        raise HTTPException(status_code=404, detail="QR code not found")
    return {"message": "QR code deleted"}

@app.get("/qr", response_model=list[schemas.QRCode])
def list_qr_codes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_qr_codes(db, skip=skip, limit=limit)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
