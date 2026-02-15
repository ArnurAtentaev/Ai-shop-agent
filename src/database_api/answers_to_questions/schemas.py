from .base_schemas import QuestionBaseSchema, AnswerToQuestionBaseSchema


class GetQuestionSchema(QuestionBaseSchema):
    pass


class CreateQuestionSchema(QuestionBaseSchema):
    pass


class CreateAnswerToQuestionSchema(AnswerToQuestionBaseSchema):
    pass


class GetAnswerToQuestionSchema(AnswerToQuestionBaseSchema):
    pass
