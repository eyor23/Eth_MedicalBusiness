from sqlalchemy import Column, Integer, String, Float
from database import Base

class Detection(Base):
    __tablename__ = 'detections'

    id = Column(Integer, primary_key=True, index=True)
    bbox = Column(String)  # Store as a comma-separated string
    confidence = Column(Float)
    class_label = Column(String)
