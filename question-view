from app.models import Question
from config import db
from sqlalchemy.exc import SQLAlchemyError

def create_question(text):
    try:
        question = Question(text=text)
        db.session.add(question)
        db.session.commit()
        return question
    except SQLAlchemyError as e:
        db.session.rollback()
        # 로깅 또는 에러 메시지 반환 등 추가 처리를 할 수 있음
        print(f"Error creating question: {e}")
        return None
