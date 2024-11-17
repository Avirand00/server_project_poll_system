from pydantic import BaseModel


class UserQuestionResult(BaseModel):
    title: str
    answer: str
