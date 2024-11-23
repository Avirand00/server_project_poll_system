from typing import List
from fastapi import HTTPException
from starlette import status
from api.internalApi.userService import user_service_api
from model.answer import Answer
from model.answer_request import AnswerRequest
from model.answer_response import AnswerResponse
from model.poll_question_results import PollQuestionResults
from model.user_poll_result import UserQuestionResult
from repository import answer_repository
from service import question_service


async def create_user_answers(user_id, answer_request: List[AnswerRequest]):
    answers = []
    last_question_id = []
    for user_answer in answer_request:
        if user_answer.question_id in last_question_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Question {user_answer.question_id} appears more than once")

        else:
            exist_answer = await check_answer_exist(user_id, user_answer)
            if exist_answer:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"User already answered question {user_answer.question_id}")

            exist_question = await question_service.get_question_by_id(user_answer.question_id)
            if not exist_question:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Question {user_answer.question_id} Not Found")

            allowed_answers = [1, 2, 3, 4]
            if user_answer.answer not in allowed_answers:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"No such option: {user_answer.answer}")

            answer = Answer(user_id=user_id,
                            question_id=user_answer.question_id,
                            answer=user_answer.answer)

            answers.append(answer)
            last_question_id.append(user_answer.question_id)

    for answer in answers:
        await answer_repository.create_answer(answer)


async def update_answer(user_id: int, answer_request: List[AnswerRequest]):
    answers = []
    last_question_id = []
    for user_answer in answer_request:
        if user_answer.question_id in last_question_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Question {user_answer.question_id} appears more than once")

        else:
            exist_question = await question_service.get_question_by_id(user_answer.question_id)
            if not exist_question:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Question {user_answer.question_id} Not Found")

            exist_answer = await check_answer_exist(user_id, user_answer)
            if not exist_answer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"No answer for question: {user_answer.question_id}")

            allowed_answers = [1, 2, 3, 4]
            if user_answer.answer not in allowed_answers:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Question: {user_answer.question_id} No such option: {user_answer.answer}")

            answer = Answer(user_id=user_id,
                            question_id=user_answer.question_id,
                            answer=user_answer.answer)

            answers.append(answer)
            last_question_id.append(answer.question_id)

    for answer in answers:
        await answer_repository.update_answer(user_id, answer)


async def check_user_exist_and_registered_by_id(user_id: int) -> bool:
    user = await user_service_api.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {user_id} Not Found")

    if not user.is_registered:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User {user_id} Not Registered")

    return True


async def check_answer_exist(user_id: int, answer: AnswerRequest) -> bool:
    question_id = answer.question_id
    return await answer_repository.get_answer_by_user_question(user_id, question_id)


async def get_all_answers() -> List[AnswerResponse]:
    results = await answer_repository.get_all_answers()
    return [AnswerResponse(user_id=result.user_id,
                           question_id=result.question_id,
                           answer=result.answer) for result in results]


async def get_poll_results() -> List[PollQuestionResults]:
    questions = await question_service.get_all_questions()
    results = []
    for question in questions:
        question_id = question.id
        question_result = await get_poll_question_results_by_question_id(question_id)
        results.append(question_result)

    return results


async def get_poll_question_total_answers_by_question_id(question_id: int) -> str:
    exist_question = await question_service.get_question_by_id(question_id)
    if not exist_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question {question_id} Not Found")

    answers = await answer_repository.get_all_question_answers(question_id)
    return f"Total answers for question {question_id}: {len(answers)}"


async def get_poll_question_results_by_question_id(question_id: int) -> PollQuestionResults:
    exist_question = await question_service.get_question_by_id(question_id)
    if not exist_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question {question_id} Not Found")

    answers = await answer_repository.get_all_question_answers(question_id)
    results = [0, 0, 0, 0]

    for i in range(0, 4):
        for question_answer in answers:
            if question_answer.answer == i+1:
                results[i] += 1

    question_results = PollQuestionResults(question_id=question_id,
                                           title=exist_question.title,
                                           option_1=exist_question.option_1,
                                           option_1_result=results[0],
                                           option_2=exist_question.option_2,
                                           option_2_result=results[1],
                                           option_3=exist_question.option_3,
                                           option_3_result=results[2],
                                           option_4=exist_question.option_4,
                                           option_4_result=results[3])
    return question_results


async def get_poll_results_by_user_id(user_id: int) -> List[UserQuestionResult]:
    exist_user = await user_service_api.get_user_by_id(user_id)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {user_id} Not Found")

    answers = await answer_repository.get_all_user_answers(user_id)
    user_answers_with_text = []
    for answer in answers:
        question_result = await answer_to_text_answer(answer)
        user_answers_with_text.append(question_result)

    return user_answers_with_text


async def get_poll_user_total_answers_by_user_id(user_id: int) -> str:
    exist_user = await user_service_api.get_user_by_id(user_id)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {user_id} Not Found")

    answers = await answer_repository.get_all_user_answers(user_id)
    return f"Total answers for user: {user_id} are: {len(answers)}"


async def answer_to_text_answer(answer: Answer) -> UserQuestionResult:
    answer_text = ""
    question = await question_service.get_question_by_id(answer.question_id)
    if answer.answer == 1:
        answer_text = question.option_1
    elif answer.answer == 2:
        answer_text = question.option_2
    elif answer.answer == 3:
        answer_text = question.option_3
    elif answer.answer == 4:
        answer_text = question.option_4
    return UserQuestionResult(title=question.title, answer=answer_text)


async def delete_answer_by_id(answer_id: int):
    await answer_repository.delete_answer_by_id(answer_id)


async def delete_all_question_answers_by_question_id(question_id: int):
    exist_question = await question_service.get_question_by_id(question_id)
    if not exist_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question: {question_id} Not Found")

    await answer_repository.delete_all_question_answers_by_question_id(question_id)


async def delete_all_user_answers_by_user_id(user_id: int):
    exist_user = await user_service_api.get_user_by_id(user_id)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User: {user_id} Not Found")

    await answer_repository.delete_all_user_answers_by_user_id(user_id)
