from typing import Optional
from pydantic import BaseModel


class Answer(BaseModel):
    id: Optional[int] = None
    user_id: int
    question_id: int
    answer: int
