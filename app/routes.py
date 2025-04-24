from flask import Blueprint, request, jsonify
from app.services.users import create_user

# 사용자 회원가입용 블루프린트 생성
routes = Blueprint('user_bp', __name__)

@routes.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()
    name = data.get('name')       # 이름
    email = data.get('email')     # 이메일
    age = data.get('age')         # 나이
    gender = data.get('gender')   # 성별

    # create_user 함수 호출로 사용자 생성
    user = create_user(name, email, gender, age)

    # 성공 시 응답 메시지와 사용자 ID 반환
    return jsonify({
        "message": f"{user.name}님 회원가입을 축하합니다",
        "user_id": user.id
    }), 200
