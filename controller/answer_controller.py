from typing import List
from fastapi import APIRouter
from starlette import status
from model.answer_request import AnswerRequest
from model.answer_response import AnswerResponse
from model.poll_question_results import PollQuestionResults
from model.user_poll_result import UserQuestionResult
from service import answer_service

router = APIRouter(
    prefix="/poll",
    tags=["poll"],
    responses={401: {"poll": "Not authorized"}}
)


@router.post("/user/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_user_answers(user_id: int, answer_request: List[AnswerRequest]):
    if await answer_service.check_user_exist_and_registered_by_id(user_id):
        await answer_service.create_user_answers(user_id, answer_request)


@router.put("/user/{user_id}")
async def update_user_answer(user_id: int, answer_request: List[AnswerRequest]):
    await answer_service.update_answer(user_id, answer_request)


@router.get("/", response_model=List[AnswerResponse])
async def get_all_answers():
    return await answer_service.get_all_answers()


@router.get("/results/", response_model=List[PollQuestionResults])
async def get_all_poll_results():
    return await answer_service.get_poll_results()


@router.get("/question/results/{question_id}", response_model=PollQuestionResults)
async def get_poll_results_by_question_id(question_id: int):
    return await answer_service.get_poll_question_results_by_question_id(question_id)


@router.get("/question/total/{question_id}", response_model=str)
async def get_poll_question_total_answers_by_question_id(question_id: int):
    return await answer_service.get_poll_question_total_answers_by_question_id(question_id)


@router.get("/user/{user_id}", response_model=List[UserQuestionResult])
async def get_poll_results_by_user_id(user_id: int):
    return await answer_service.get_poll_results_by_user_id(user_id)


@router.get("/user/total/{user_id}", response_model=str)
async def get_poll_user_total_answers_by_user_id(user_id: int):
    return await answer_service.get_poll_user_total_answers_by_user_id(user_id)


@router.delete("/answer/{answer_id}", status_code=status.HTTP_200_OK)
async def delete_answer_by_id(answer_id: int):
    await answer_service.delete_answer_by_id(answer_id)


@router.delete("/question/{question_id}", status_code=status.HTTP_200_OK)
async def delete_all_question_answers_by_question_id(question_id: int):
    await answer_service.delete_all_question_answers_by_question_id(question_id)


@router.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_all_user_answers_by_user_id(user_id: int):
    await answer_service.delete_all_user_answers_by_user_id(user_id)
