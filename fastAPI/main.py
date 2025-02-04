from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import sys
import logging

# Add the current directory to the sys.path to allow absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import crud
import model_detection as models_detection
import schema as schemas_detection

import crud_telegram
import model_telegram as models_telegram
import telegram_schema as schemas_telegram

from database import SessionLocal, engine

models_detection.Base.metadata.create_all(bind=engine)
models_telegram.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Detection Endpoints
@app.post("/detections/", response_model=schemas_detection.Detection)
def create_detection(detection: schemas_detection.DetectionCreate, db: Session = Depends(get_db)):
    try:
        created_detection = crud.create_detection(db=db, detection=detection)
        logging.info(f'Created detection: {created_detection}')
        return created_detection
    except ValueError as e:
        logging.error(f'ValueError: {e}')
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f'Exception: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')

@app.get("/detections/", response_model=list[schemas_detection.Detection])
def read_detections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    detections = crud.get_detections(db, skip=skip, limit=limit)
    return detections

@app.get("/detections/{detection_id}", response_model=schemas_detection.Detection)
def read_detection(detection_id: int, db: Session = Depends(get_db)):
    detection = crud.get_detection(db, detection_id=detection_id)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection

@app.put("/detections/{detection_id}", response_model=schemas_detection.Detection)
def update_detection(detection_id: int, detection: schemas_detection.DetectionUpdate, db: Session = Depends(get_db)):
    updated_detection = crud.update_detection(db=db, detection_id=detection_id, detection=detection)
    if updated_detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return updated_detection

@app.delete("/detections/{detection_id}", response_model=schemas_detection.Detection)
def delete_detection(detection_id: int, db: Session = Depends(get_db)):
    deleted_detection = crud.delete_detection(db=db, detection_id=detection_id)
    if deleted_detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return deleted_detection

# Telegram Message Endpoints
@app.post("/messages/", response_model=schemas_telegram.TelegramMessage)
def create_message(message: schemas_telegram.TelegramMessageCreate, db: Session = Depends(get_db)):
    try:
        created_message = crud_telegram.create_message(db=db, message=message)
        logging.info(f'Created message: {created_message}')
        return created_message
    except ValueError as e:
        logging.error(f'ValueError: {e}')
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f'Exception: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')

@app.get("/messages/", response_model=list[schemas_telegram.TelegramMessage])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud_telegram.get_messages(db, skip=skip, limit=limit)
    return messages

@app.get("/messages/{message_id}", response_model=schemas_telegram.TelegramMessage)
def read_message(message_id: int, db: Session = Depends(get_db)):
    message = crud_telegram.get_message(db, message_id=message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.put("/messages/{message_id}", response_model=schemas_telegram.TelegramMessage)
def update_message(message_id: int, message: schemas_telegram.TelegramMessageUpdate, db: Session = Depends(get_db)):
    updated_message = crud_telegram.update_message(db=db, message_id=message_id, message=message)
    if updated_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message

@app.delete("/messages/{message_id}", response_model=schemas_telegram.TelegramMessage)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    deleted_message = crud_telegram.delete_message(db=db, message_id=message_id)
    if deleted_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return deleted_message
