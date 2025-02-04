from sqlalchemy.orm import Session
import model_detection as models
import schema as schemas

def get_detection(db: Session, detection_id: int):
    db_detection = db.query(models.Detection).filter(models.Detection.id == detection_id).first()
    if db_detection:
        bbox_list = list(map(float, db_detection.bbox.split(',')))
        return schemas.Detection(
            id=db_detection.id,
            bbox=bbox_list,
            confidence=db_detection.confidence,
            class_label=db_detection.class_label,
        )
    return None

def get_detections(db: Session, skip: int = 0, limit: int = 100):
    db_detections = db.query(models.Detection).offset(skip).limit(limit).all()
    detections = []
    for db_detection in db_detections:
        bbox_list = list(map(float, db_detection.bbox.split(',')))
        detection = schemas.Detection(
            id=db_detection.id,
            bbox=bbox_list,
            confidence=db_detection.confidence,
            class_label=db_detection.class_label,
        )
        detections.append(detection)
    return detections

def create_detection(db: Session, detection: schemas.DetectionCreate):
    bbox_str = ','.join(map(str, detection.bbox))
    db_detection = models.Detection(bbox=bbox_str, confidence=detection.confidence, class_label=detection.class_label)
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return get_detection(db, db_detection.id)

def update_detection(db: Session, detection_id: int, detection: schemas.DetectionUpdate):
    db_detection = db.query(models.Detection).filter(models.Detection.id == detection_id).first()
    if db_detection:
        if detection.bbox:
            db_detection.bbox = ','.join(map(str, detection.bbox))
        if detection.confidence is not None:
            db_detection.confidence = detection.confidence
        if detection.class_label:
            db_detection.class_label = detection.class_label
        db.commit()
        db.refresh(db_detection)
        return get_detection(db, db_detection.id)
    return None

def delete_detection(db: Session, detection_id: int):
    db_detection = db.query(models.Detection).filter(models.Detection.id == detection_id).first()
    if db_detection:
        db.delete(db_detection)
        db.commit()
        return get_detection(db, db_detection.id)
    return None
