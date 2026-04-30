from sqlalchemy.orm import Session
from . import models, schemas
import secrets
import string
from datetime import datetime

def generate_short_token(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_qr_code(db: Session, qr_code: schemas.QRCodeCreate):
    short_token = generate_short_token()
    while get_qr_code_by_token(db, short_token):
        short_token = generate_short_token()
    
    db_qr = models.QRCode(
        short_token=short_token,
        original_url=str(qr_code.original_url),
        expires_at=qr_code.expires_at
    )
    db.add(db_qr)
    db.commit()
    db.refresh(db_qr)
    return db_qr

def get_qr_code_by_token(db: Session, token: str):
    return db.query(models.QRCode).filter(models.QRCode.short_token == token, models.QRCode.deleted_at.is_(None)).first()

def get_qr_codes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.QRCode).filter(models.QRCode.deleted_at.is_(None)).offset(skip).limit(limit).all()

def update_qr_code(db: Session, token: str, qr_code_update: schemas.QRCodeUpdate):
    db_qr = get_qr_code_by_token(db, token)
    if db_qr:
        update_data = qr_code_update.dict(exclude_unset=True)
        if 'original_url' in update_data:
            update_data['original_url'] = str(update_data['original_url'])
        for key, value in update_data.items():
            setattr(db_qr, key, value)
        db.commit()
        db.refresh(db_qr)
    return db_qr

def delete_qr_code(db: Session, token: str):
    db_qr = get_qr_code_by_token(db, token)
    if db_qr:
        db_qr.deleted_at = datetime.utcnow()
        db.commit()
    return db_qr