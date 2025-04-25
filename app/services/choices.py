from app.models import db, Question, Choices
from sqlalchemy.exc import SQLAlchemyError

# 특정 질문의 선택지 조회
def get_choices(question_id):
    return [choice.to_dict() for choice in Choices.query.filter_by(question_id=question_id).all()]

# 선택지 생성
def create_choices(content, sqe, question_id, is_active = True):
    try:
        choice = Choices(
            content = content,
            sqe = sqe,
            question_id = question_id,
            is_active = is_active
        )
        db.session.add(choice)
        db.session.commit()
        return choice
    except SQLAlchemyError:
        db.session.rollback()
        return None