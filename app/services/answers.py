from app.models import Answer, User, db
from sqlalchemy.exc import SQLAlchemyError

# 사용자의 답변 저장
def submit_answer(user_id, choice_id):
    try:
        answer = Answer(
            user_id = user_id,
            choice_id = choice_id
        )
        
        db.session.add(answer)
        db.session.commit()
        return answer
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

# 사용자 답변 조회 
def get_answer(user_id):
    return [answer.to_dict() for answer in Answer.query.filter_by(user_id=user_id).all()]