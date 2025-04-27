from pydantic import BaseModel
from datetime import datetime

class STask(BaseModel):
    number: int
    title: str
    description: str
    date_create: datetime

    class Config:
        orm_mode = True