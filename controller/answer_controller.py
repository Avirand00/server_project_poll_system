from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status

from model.answer import Answer
from model.answer_request import AnswerRequest
from model.question import Question
from service import question_service, answer_service

router = APIRouter(
    prefix="/answer",
    tags=["answer"],
    responses={401: {"answer": "Not authorized"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_answer(answer: Answer):
    exist_user = await answer_service.check_user_exist(answer.user_id)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {answer.user_id} Not Found")
    try:
        await answer_service.create_answer(answer)
    except Exception as e:
        error_details = str(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_details)


@router.post("/user/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_user_answer(user_id: int, answer_request: List[AnswerRequest]):
    exist_user = await answer_service.check_user_exist(user_id)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {user_id} Not Found")
    for answer in answer_request:
        user_answer = Answer(user_id=user_id,
                             question_id= answer.question_id,
                             answer=answer.answer)
        try:
            await answer_service.create_answer(user_answer)
        except Exception as e:
            error_details = str(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=error_details)


@router.get("/")
async def get_all_answers():
    pass


@router.get("/{question_id}")
async def get_answers_by_question_id():
    pass


@router.get("/{user_id}")
async def get_answers_by_user_id():
    pass


