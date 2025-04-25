from flask import Blueprint, jsonify, request, abort
from app.services.images import create_image
from app.services.questions import get_question_by_id, get_all_questions
from app.services.users import create_user
from app.services.answers import submit_answer
from app.services.choices import get_choices
from app.models import Image,Choices,Question
from config import db

# 사용자 회원가입용 블루프린트 생성
bp = Blueprint("routes", __name__)

# 기본 연결 확인
@bp.route('/', methods = ["GET"])
def get_API():
    return jsonify({"message": "Success Connect"})

# 메인 이미지 가져오기
@bp.route('/image/main', methods = ["GET"])
def get_main_image():
    main_image = Image.query.filter_by(type="main").first()
    if not main_image:
        return jsonify({"error": "Main image not found"}), 404
    return jsonify({"image": main_image.url})

# 질문 가져오기
@bp.route('/questions/<int:question_id>', methods = ['GET'])
def get_question(question_id):
    question = get_question_by_id(question_id)
    if question:
        return jsonify(question)
    else:
        return jsonify({"error": "Question not found"}), 404
    
# 질문 개수 확인
@bp.route('/questions/count', methods = ["GET"])
def get_question_count(question_id):
    all_questions = get_all_questions(question_id)
    return jsonify({"total": len(all_questions)})
    
# 선택지 가져오기
@bp.route('/choice/<int:question_id>', methods = ["GET"])
def get_choice(question_id):
    choice = get_choices(question_id)
    return jsonify({"choices": choice})


# 답변 제출하기
@bp.route('/submit', methods = ["POST"])
def submit_choice():
    data = request.get_json()
    user_id = None # 공통으로 사용될 user_id 저장용

    for item in data:
        user_id = item.get("user_id")
        choice_id = item.get("choice_id")
        result = submit_answer(user_id, choice_id)
        if result is None:
            return jsonify({"message": "Failed to create answers"})
    return jsonify({"message": f"User: {user_id}'s answers Success Create"})


# 이미지 생성
@bp.route('/image', methods = ['POST'])
def create_new_image():
    data = request.get_json()
    url = data.get("url")
    type_value = data.get("type")

    image_id = create_image(url,image_type=type_value)
    if image_id is None:
        return jsonify({"Message": "Failed to create image"})
    return jsonify({"message": f"ID: {image_id} Image Success Create"}), 201

# 질문 생성
@bp.route('/question', methods = ["POST"])
def create_question():
    data = request.get_json()
    title = data.get('title')
    sqe = data.get('sqe')
    image_id = data.get('image_id')
    is_active = data.get('is_active', True)  

    if not title or sqe is None or not image_id:
        abort(400, "필수 값이 누락되었습니다: title, sqe, image_id")

    question = Question(title=title, sqe=sqe, image_id=image_id, is_active=is_active)

    db.session.add(question)
    db.session.commit()
    # 성공시 메시지와 생성한 질문 id와 내용을 보여줌
    return jsonify({
        "message":  f"Title: {question.id} question Success Create",
        "question": {
            "id": question.id,
            "title": question.title,
            "sqe": question.sqe,
            "image_id": question.image_id
        }
    }), 201

# 선택지 생성
@bp.route('/choice', methods=["POST"])
def create_choice():
    data = request.get_json()
    content = data.get('content')  #선택지 내용         
    sqe = data.get('sqe')  # 선택지 순서                 
    question_id = data.get('question_id')  # 어떤 질문의 선택지인지  
    is_active = data.get('is_active', True)

    # content, sqe, question_id 이 빠졌을때 오류
    if not content or sqe is None or not question_id:
        abort(400, "필수 값이 누락되었습니다: content, sqe, question_id")

    choice = Choices(content=content, sqe=sqe, question_id=question_id, is_active=is_active)

    db.session.add(choice)   # 선택지를 DB에 추가
    db.session.commit()      # 실제로 저장
    # 성공 시 메세지와 딕셔너리 형태로 변환해서 JSON으로 보여줌
    return jsonify({
        "message": f"Content: {choice.id} choice Success",
        "choice": choice.to_dict()  
    }), 201

# 회원가입
@bp.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()
    name = data.get('name')       # 이름
    email = data.get('email')     # 이메일
    age = data.get('age')         # 나이
    gender = data.get('gender')   # 성별

    # create_user 함수 호출로 사용자 생성
    user = create_user(name, email, gender, age)

    # 성공 시 응답 메시지와 사용자 ID 반환
    # 이미 app/__init__.py에서 아래와 같이 400 에러를 JSON으로 반환하도록 핸들러를 등록되어 있어 설정 X
    return jsonify({
        "message": f"{user.name}님 회원가입을 축하합니다",
        "user_id": user.id
    }), 200
