from sqladmin import ModelView

from multiple_choice_questions.models.question_model import Question
from multiple_choice_questions.models.choice_model import Choice


class QuestionAdmin(ModelView, model=Question):
    name = "Question"
    page_size_options = [25, 50, 100, 200]
    category = "Multiple Choice Questions"

    can_create = False
    can_delete = True

    column_list = [
        Question.id,
        Question.question,
        Question.explanation,
        Question.created_at,
        Question.updated_at,
    ]

    form_excluded_columns = [
        Question.choices
    ]
