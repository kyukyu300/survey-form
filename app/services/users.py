#사용자 조회 만들기
from config import db
from app.models import User

#아이디로 조회
def get_user_by_id(user_id):
    return User.query.get(user_id)

#이메일로 조회
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

#전체 조회
def get_all_users():
    return User.query.all()
from config import db
from app.models import User


def create_user(name, email, gender, age):
    # User 모델 인스턴스 생성 (named 매개변수 방식)
    user = User(name=name, email=email, gender=gender, age=age)

    # 세션에 추가 후 커밋하여 데이터베이스에 반영
    db.session.add(user)
    db.session.commit()

    return user
