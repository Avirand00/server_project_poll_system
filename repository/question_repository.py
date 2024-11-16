from typing import Optional, List

from model.question import Question
from repository.database import database

TABLE_NAME = "question"


async def create_question(question: Question) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (title, option_1, option_2, option_3, option_4)
        VALUES (:title, :option_1, :option_2, :option_3, :option_4)
        """
    values = {"title": question.title,
              "option_1": question.option_1,
              "option_2": question.option_2,
              "option_3": question.option_3,
              "option_4": question.option_4}
    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")

    question.id = last_record_id[0]
    return question.id


async def get_question_by_id(question_id: int) -> Optional[Question]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE id=:id"
    return await database.fetch_one(query, values={"id": question_id})


async def get_all_questions() -> List[Question]:
    query = f"SELECT * FROM {TABLE_NAME}"
    return await database.fetch_all(query)


async def update_question_by_id(question_id: int, question: Question):
    query = f"""
    UPDATE {TABLE_NAME}
    SET title = :title,
    option_1 = :option_1,
    option_2 = :option_2,
    option_3 = :option_3,
    option_4 = :option_4
    WHERE id = :question_id
    """

    values = {"title": question.title,
              "option_1": question.option_1,
              "option_2": question.option_2,
              "option_3": question.option_3,
              "option_4": question.option_4,
              "question_id": question_id}

    await database.execute(query, values)


async def delete_question(question_id):
    query = f"DELETE FROM {TABLE_NAME} WHERE id=:question_id"
    await database.execute(query, values={"question_id": question_id})
