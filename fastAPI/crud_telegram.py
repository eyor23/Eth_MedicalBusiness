from sqlalchemy.orm import Session
import model_telegram as models
import telegram_schema as schemas

def get_message(db: Session, message_id: int):
    return db.query(models.TelegramMessage).filter(models.TelegramMessage.id == message_id).first()

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TelegramMessage).offset(skip).limit(limit).all()

def create_message(db: Session, message: schemas.TelegramMessageCreate):
    db_message = models.TelegramMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_message(db: Session, message_id: int, message: schemas.TelegramMessageUpdate):
    db_message = db.query(models.TelegramMessage).filter(models.TelegramMessage.id == message_id).first()
    if db_message:
        for key, value in message.dict(exclude_unset=True).items():
            setattr(db_message, key, value)
        db.commit()
        db.refresh(db_message)
        return db_message
    return None

def delete_message(db: Session, message_id: int):
    db_message = db.query(models.TelegramMessage).filter(models.TelegramMessage.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
        return db_message
    return None
