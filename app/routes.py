from flask import Blueprint, request, jsonify
from app.services.users import create_user

# 사용자 회원가입용 블루프린트 생성
routes = Blueprint('user_bp', __name__)

@routes.route('/users', methods=['POST'])
def create_user_route():

    data = request.get_json()
    name = data.get('name')       # 이름
    email = data.get('email')     # 이메일
    gender = data.get('gender')   # 성별
    age = data.get('age')         # 나이

    # create_user 함수 호출로 사용자 생성
    user = create_user(name, email, gender, age)

    # 생성된 사용자 정보를 JSON으로 반환
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "gender": user.gender,
        "age": user.age
    }), 201