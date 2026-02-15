from pydantic import BaseModel


class QuestionBaseSchema(BaseModel):
    question: str
    answer: str


class AnswerToQuestionBaseSchema(BaseModel):
    answer_chunks: str
