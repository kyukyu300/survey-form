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