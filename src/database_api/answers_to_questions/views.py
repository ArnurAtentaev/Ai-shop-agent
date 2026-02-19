from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from database_api.answers_to_questions import crud
from database_api.answers_to_questions.schemas import (
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
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    models = request.app.state.models
    return await crud.create_questions(
        session=session, question_in=question_in, models=models
    )
