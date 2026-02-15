from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.initialize_models import embedding_model
from src.utils.database_utils import chunking
from .schemas import CreateQuestionSchema
from src.core.models import Question, AnswerToQuestion


async def create_questions(
    session: AsyncSession,
    question_in: CreateQuestionSchema,
):

    question_dict = question_in.model_dump()
    embeddings = embedding_model.encode(question_dict["question"])

    question = Question(
        questions=question_dict["question"],
        question_embeddings=embeddings,
    )
    session.add(question)
    await session.flush()

    chunks = chunking(text=question_dict["answer"])

    answers = [
        AnswerToQuestion(
            question_id=question.id,
            answer_chunks=chunk,
        )
        for chunk in chunks
    ]
    session.add_all(answers)

    await session.commit()
    return {
        "id": question.id,
        "question": question_dict["question"],
        "answer": question_dict["answer"],
    }
