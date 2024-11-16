from pydantic import BaseModel


class UserQuestionResult(BaseModel):
    question_id: int
    title: str
    answer: int
    answer_text: str
