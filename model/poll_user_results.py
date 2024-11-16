from typing import List
from pydantic import BaseModel
from model.user_poll_result import UserQuestionResult


class PollUserResults(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    total_questions_answered: int
    poll_results: List[UserQuestionResult]
