from pydantic import BaseModel


class AnswerResponse(BaseModel):
    user_id: int
    question_id: int
    answer: int
