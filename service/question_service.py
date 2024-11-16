from typing import Optional, List

from fastapi import HTTPException
from starlette import status

from model.question import Question
from repository import question_repository


async def create_question(question: Question) -> int:
    return await question_repository.create_question(question)


async def get_question_by_id(question_id: int) -> Optional[Question]:
    exist_question = await question_repository.get_question_by_id(question_id)
    if not exist_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question {question_id} Not Found")

    return exist_question


async def get_all_questions() -> List[Question]:
    return await question_repository.get_all_questions()


async def update_question_by_id(question_id: int, question: Question):
    await get_question_by_id(question_id)
    await question_repository.update_question_by_id(question_id, question)


async def delete_question_by_id(question_id: int):
    await get_question_by_id(question_id)
    try:
        await question_repository.delete_question(question_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Question has been answered by users. Delete user answers first")
