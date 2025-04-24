from flask import Blueprint, jsonify, request
from app.services.images import get_all_image, create_image
from app.services.questions import get_question_by_id, get_all_questions

bp = Blueprint("routes", __name__)

# 기본 연결 확인
@bp.route('/', methods = ["GET"])
def get_API():
    return jsonify({"message": "Success Connect"})

# 메인 이미지 가져오기
@bp.route('/image/main', methods = ["GET"])
def get_image():
    all_image = get_all_image()
    return jsonify({"image": all_image[0].url})

# 질문 가져오기
@bp.route('/questions/<int:question_id>', methods = ['GET'])
def get_question():
    question = get_question_by_id()
    if question:
        return jsonify(question)
    else:
        return jsonify({"error": "Question not found"}), 404
    
# 질문 개수 확인
@bp.route('/questions/count', methods = ["GET"])
def get_question_count():
    all_questions = get_all_questions()
    return jsonify({"total": all_questions.count()})
    
# 선택지 가져오기
@bp.route('/choice/<int:question_id>', methods = ["GET"])
def get_choice():
    pass

# 답변 제출하기
@bp.route('/submit', methods = ["POST"])
def submit_choice():
    data = request.get_json()
    pass
    # user_id = 함수(data)
    #return jsonify({"message": f"User: {user_id}'s answers Success Create"})


# 이미지 생성
@bp.route('/image', methods = ['POST'])
def create_new_image():
    data = request.get_json()
    url = data.get("url")

    image_id = create_image(url)
    return jsonify({"message": f"ID: {image_id} Image Success Create"}), 201

# 질문 생성
@bp.route('/question', methods = ["POST"])
def create_question():
    pass

# 선택지 생성
@bp.route('/choice', methods = ["POST"])
def create_choice():
    pass