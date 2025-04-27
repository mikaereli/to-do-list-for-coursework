import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_create = Column(DateTime, nullable=False, default=datetime.datetime.now)