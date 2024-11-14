from fastapi import APIRouter, HTTPException
from starlette import status
from model.question import Question
from service import question_service

router = APIRouter(
    prefix="/question",
    tags=["question"],
    responses={401: {"question": "Not authorized"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=int)
async def create_question(question: Question):
    return await question_service.create_question(question)


@router.get("/{question_id}", status_code=status.HTTP_200_OK)
async def get_question_by_id(question_id: int):
    exist_question = await question_service.get_by_id(question_id)
    if not exist_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question {question_id} Not Found")
    return exist_question


@router.put("/{question_id}")
async def update_question(question_id: int, question: Question):
    exist_question = await question_service.get_by_id(question_id)
    if not exist_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Question {question_id} Not Found")
    await question_service.update_question_by_id(question_id, question)


@router.delete("/{question_id}", status_code=status.HTTP_200_OK)
async def delete_question(question_id: int):
    exist_question = await question_service.get_by_id(question_id)
    if not exist_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question {question_id} Not Found")
    await question_service.delete_question_by_id(question_id)


