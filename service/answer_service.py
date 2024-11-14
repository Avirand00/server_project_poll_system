from typing import List

from fastapi import HTTPException
from starlette import status

from api.internalApi.userService import user_service_api
from model.answer import Answer
from model.answer_request import AnswerRequest
from repository import answer_repository
from service import question_service


async def create_answer(user_answer: Answer):
    exist_answer = await check_answer_exist(user_answer)
    if exist_answer:
        raise Exception(f"User already answered this question")

    exist_question = await question_service.get_by_id(user_answer.question_id)
    if not exist_question:
        raise Exception(f"Question {user_answer.question_id} Not Found")
    await answer_repository.create_answer(user_answer)


async def check_user_exist(user_id: int) -> bool:
    return await user_service_api.check_exist_user_by_id(user_id)


async def check_answer_exist(answer: Answer) -> bool:
    user_id = answer.user_id
    question_id = answer.question_id
    return await answer_repository.get_answer_by_user_question(user_id, question_id)

async def post_user_answers(user_id: int, answer_request: List[AnswerRequest]):
    for answer in answer_request:
        user_answer = Answer(user_id=user_id,
                             question_id=answer.question_id,
                             answer=answer.answer)
        await create_answer(user_answer)