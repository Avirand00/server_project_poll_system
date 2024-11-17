from pydantic import BaseModel


class PollQuestionResults(BaseModel):
    question_id: int
    title: str
    option_1: str
    option_1_result: int
    option_2: str
    option_2_result: int
    option_3: str
    option_3_result: int
    option_4: str
    option_4_result: int
