from typing import List
from model.answer import Answer
from repository.database import database

TABLE_NAME = "user_answer"


async def create_answer(user_answer: Answer):
    query = f"""
    INSERT INTO {TABLE_NAME} (user_id, question_id, answer)
    VALUES (:user_id, :question_id, :answer)
    """

    values = {"user_id": user_answer.user_id,
              "question_id": user_answer.question_id,
              "answer": user_answer.answer}

    await database.execute(query, values)


async def update_answer(user_id: int, user_answer: Answer):
    query = f"UPDATE {TABLE_NAME} SET answer=:answer WHERE user_id=:user_id AND question_id=:question_id"
    values = {"answer": user_answer.answer,
              "user_id": user_id,
              "question_id": user_answer.question_id}
    await database.execute(query, values)


async def get_all_answers() -> List[Answer]:
    query = f"SELECT * FROM {TABLE_NAME}"
    return await database.fetch_all(query)


async def get_answer_by_user_question(user_id: int, question_id: int) -> bool:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id=:user_id AND question_id=:question_id"
    values = {"user_id": user_id, "question_id": question_id}
    return await database.fetch_one(query, values)


async def get_all_question_answers(question_id: int) -> List[Answer]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE question_id=:question_id"
    results = await database.fetch_all(query, values={"question_id": question_id})
    return [Answer(**result) for result in results]


async def get_all_user_answers(user_id: int) -> List[Answer]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id=:user_id"
    results = await database.fetch_all(query, values={"user_id": user_id})
    return [Answer(**result) for result in results]


async def delete_answer_by_id(answer_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE id=:answer_id"
    await database.execute(query, values={"answer_id": answer_id})


async def delete_all_question_answers_by_question_id(question_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE question_id=:question_id"
    await database.execute(query, values={"question_id": question_id})


async def delete_all_user_answers_by_user_id(user_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE user_id=:user_id"
    await database.execute(query, values={"user_id": user_id})
