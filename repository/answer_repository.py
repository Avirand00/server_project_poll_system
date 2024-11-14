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


async def get_answer_by_user_question(user_id: int, question_id: int) -> bool:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id=:user_id AND question_id=:question_id"
    values = {"user_id": user_id, "question_id": question_id}
    result = await database.fetch_one(query, values)
    if result:
        return True
    else:
        return False



