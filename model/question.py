from typing import Optional
from pydantic import BaseModel


class Question(BaseModel):
    id: Optional[int] = None
    title: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
