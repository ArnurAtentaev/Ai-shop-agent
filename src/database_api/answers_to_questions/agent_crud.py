import logging

from src.core.models.db import db_helper
from src.core.models import AnswerToQuestion, Question
from src.utils.database_utils import reranker
from src.agent.initialize_models import embedding_model

from langchain_core.tools import tool
from sqlalchemy import FLOAT, select, cast
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)


@tool
async def get_general_answer(query: str):
    """General questions answered."""

    query_vector = embedding_model.encode(
        query,
        normalize_embeddings=True,
    )
    session = db_helper.get_scoped_session()

    try:
        distance = cast(Question.question_embeddings.op("<=>")(query_vector), FLOAT)
        stmt = (
            select(
                AnswerToQuestion.answer_chunks,
            )
            .join(Question, Question.id == AnswerToQuestion.question_id)
            .where(distance < 0.2)
            .order_by(distance)
            .limit(5)
        )
        exec = await session.execute(stmt)
        result_execution = exec.scalars().all()
        logging.info(f"RESULT: {result_execution}")

        if result_execution is not None:
            reranked = reranker(query=query, found=result_execution)
            logging.info(f"RERANKED: {reranked}")
            return reranked

        else:
            return None

    except SQLAlchemyError as e:
        logging.exception(f"DB error in get_general_answer: {e}")

    finally:
        await session.close()
