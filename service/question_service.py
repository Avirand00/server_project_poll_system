from typing import Optional, List

from fastapi import HTTPException
from starlette import status

from model.question import Question
from repository import question_repository
from service import answer_service


async def create_question(question: Question) -> int:
    return await question_repository.create_question(question)


async def get_question_by_id(question_id: int) -> Optional[Question]:
    return await question_repository.get_question_by_id(question_id)


async def get_all_questions() -> List[Question]:
    return await question_repository.get_all_questions()


async def update_question_by_id(question_id: int, question: Question):
    exist_question = await get_question_by_id(question_id)
    if not exist_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question {question_id} Not Found")

    await question_repository.update_question_by_id(question_id, question)


async def delete_question_by_id(question_id: int):
    await answer_service.delete_all_question_answers_by_question_id(question_id)
    await question_repository.delete_question(question_id)
