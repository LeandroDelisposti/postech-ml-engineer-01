from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    sepal_length = Column(String, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_length = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    predicted_class = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)