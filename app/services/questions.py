from app.models import Question
from config import db
from sqlalchemy.exc import SQLAlchemyError

# 모든 질문 조회
def get_all_questions():
    return [q.to_dict() for q in Question.query.all()]

# 질문 하나씩 조회
def get_question_by_id(question_id):
    question = Question.query.get(question_id)
    if question:
        return question.to_dict() 
    else:
        None

# 질문 생성
def create_question(title, sqe, image_id, is_active=True):
    try:
        question = Question(
            title=title,
            sqe=sqe,
            image_id=image_id,
            is_active=is_active
        )
        db.session.add(question)
        db.session.commit()
        return question
    except SQLAlchemyError:
        db.session.rollback()
        return None