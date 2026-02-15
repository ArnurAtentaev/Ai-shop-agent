from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import db_helper
from src.database_api.answers_to_questions import crud
from src.database_api.answers_to_questions.schemas import (
    GetQuestionSchema,
    CreateQuestionSchema,
)

router_question = APIRouter(tags=["Question"])


@router_question.post(
    "/",
    response_model=GetQuestionSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_question(
    question_in: CreateQuestionSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_questions(session=session, question_in=question_in)
