from flask import Blueprint, jsonify, request, abort
from app.services.images import create_image
from app.services.questions import get_question_by_id, get_all_questions
from app.services.users import create_user
from app.services.answers import submit_answer
from app.services.choices import get_choices
from app.models import Image,Choices,Question
from config import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

# 사용자 회원가입용 블루프린트 생성
bp = Blueprint("routes", __name__)

# 기본 연결 확인
@bp.route('/', methods = ["GET"])
def get_API():
    return jsonify({"message": "Success Connect"}), 200

# 메인 이미지 가져오기
@bp.route('/image/main', methods = ["GET"])
def get_main_image():
    try:
        main_image = Image.query.filter_by(type="main").first()
        if not main_image:
            # 메인 이미지가 없을 경우 404 처리
            return jsonify({"error": "Main image not found"}), 404
        return jsonify({"image": main_image.url}), 200
    except SQLAlchemyError:
        # SQLAlchemyError: 데이터베이스 쿼리 또는 연결 오류 처리
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 기타 예기치 못한 서버 오류 처리
        return jsonify({"error": "Internal server error"}), 500

# 질문 가져오기
@bp.route('/questions/<int:question_id>', methods = ['GET'])
def get_question(question_id):
    try:
        question = get_question_by_id(question_id)
        if not question or not question.is_active:
            # 해당 ID의 질문이 없을 경우 404 처리
            return jsonify({"error": "Question not found"}), 404
        return jsonify(question.to_dict()), 200
    except SQLAlchemyError:
        # SQLAlchemyError: DB 처리 중 에러 발생 시 처리
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 예기치 못한 오류 전반 처리
        return jsonify({"error": "Internal server error"}), 500
    
# 질문 개수 확인 (활성된 항목만)
@bp.route('/questions/count', methods = ["GET"])
def get_question_count():
    # 모든 질문을 조회하여 총 개수를 반환하기 때문에 매개변수가 필요 없어서 제거
    try:
        all_questions = get_all_questions()
        return jsonify({"total": len(all_questions)}), 200
    except SQLAlchemyError:
        # SQLAlchemyError: DB 조회 오류 처리
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 기타 서버 오류 처리
        return jsonify({"error": "Internal server error"}), 500
    
# 선택지 가져오기
@bp.route('/choice/<int:question_id>', methods = ["GET"])
def get_choice(question_id):
    try:
        choice = get_choices(question_id)
        return jsonify({"choices": choice}), 200
    except SQLAlchemyError:
        # SQLAlchemyError: 선택지 조회 중 DB 오류 처리
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 기타 서버 오류 처리
        return jsonify({"error": "Internal server error"}), 500


# 답변 제출하기
@bp.route('/submit', methods = ["POST"])
def submit_choice():
    try:
        data = request.get_json()
        if not data:
            # 요청 본문이 비어있을 경우
            raise ValueError("Request body is empty")
        user_id = None
        for item in data:
            user_id = item.get("user_id")
            choice_id = item.get("choice_id")
            if not user_id or not choice_id:  # 필드 누락 검증
                raise ValueError("user_id 또는 choice_id가 누락되었습니다")
            result = submit_answer(user_id, choice_id)
            if result is None:
                # 답변 생성 실패 시
                raise ValueError("Failed to create answers")
        return jsonify({"message": f"User: {user_id}'s answers Success Create"}), 200
    except ValueError as e:
        # ValueError: 입력값 검증 실패 또는 답변 생성 실패 처리
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError:
        # SQLAlchemyError: 답변 저장 중 DB 오류 처리 및 롤백
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 예기치 못한 오류 처리 및 롤백
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


# 이미지 생성
@bp.route('/image', methods = ['POST'])
def create_new_image():
    try:
        data = request.get_json()
        url = data.get("url")
        image_type = data.get("type")
        if not url or not image_type:
            # ValueError: 필수 값 누락 시
            raise ValueError("필수 값이 누락되었습니다: url, type")
        image_id = create_image(url, image_type=image_type)   
        if image_id is None:
            # ValueError: 이미지 생성 실패 시
            raise ValueError("Failed to create image")
        return jsonify({"message": f"ID: {image_id} Image Success Create"}), 201
    except HTTPException as e:
        db.session.rollback()  # HTTPException 처리 시 세션 롤백
        return jsonify({"error": e.description}), e.code
    except ValueError as e:
        # ValueError: 입력값 검증 실패 처리
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError:
        # SQLAlchemyError: 이미지 저장 중 DB 오류 처리 및 롤백
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 기타 예기치 못한 오류 처리 및 롤백
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

# 질문 생성
@bp.route('/question', methods = ["POST"])
def create_question():
    try:
        data = request.get_json()
        title = data.get('title')
        sqe = data.get('sqe')
        image_id = data.get('image_id')
        is_active = data.get('is_active', True)
        if not title or sqe is None or not image_id:
            # ValueError: 필수 값 누락 시
            raise ValueError("필수 값이 누락되었습니다: title, sqe, image_id")
        question = Question(title=title, sqe=sqe, image_id=image_id, is_active=is_active)
        db.session.add(question)
        db.session.commit()
        return jsonify({
            "message": f"Title: {question.id} question Success Create",
            "question": {
                "id": question.id,
                "title": question.title,
                "sqe": question.sqe,
                "image_id": question.image_id
            }
        }), 201
    except ValueError as e:
        # ValueError: 입력값 검증 실패 처리
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError:
        # SQLAlchemyError: 질문 저장 중 DB 오류 처리 및 롤백
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 기타 예기치 못한 오류 처리 및 롤백
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

# 선택지 생성
@bp.route('/choice', methods=["POST"])
def create_choice():
    try:
        data = request.get_json()
        content = data.get('content')
        sqe = data.get('sqe')
        question_id = data.get('question_id')
        is_active = data.get('is_active', True)
        if not content or sqe is None or not question_id:
            # ValueError: 필수 값 누락 시
            raise ValueError("필수 값이 누락되었습니다: content, sqe, question_id")
        choice = Choices(content=content, sqe=sqe, question_id=question_id, is_active=is_active)
        db.session.add(choice)
        db.session.commit()
        return jsonify({
            "message": f"Content: {choice.id} choice Success",
            "choice": choice.to_dict()
        }), 201
    except ValueError as e:
        # ValueError: 입력값 검증 실패 처리
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError:
        # SQLAlchemyError: 선택지 저장 중 DB 오류 처리 및 롤백
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 기타 예기치 못한 오류 처리 및 롤백
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

# 회원가입
@bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        gender = data.get('gender')
        if not name or not email or age is None or not gender:
            # ValueError: 필수 값 누락 시
            raise ValueError("필수 값이 누락되었습니다: name, email, gender, age")
        user = create_user(name=name, age=age, gender=gender, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": f"{user.name}님 회원가입을 축하합니다",
            "user_id": user.id
        }), 200
    except ValueError as e:
        # ValueError: 입력값 검증 실패 처리
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError:
        # SQLAlchemyError: 회원 저장 중 DB 오류 처리
        return jsonify({"error": "Database error"}), 500
    except Exception:
        # Exception: 기타 예기치 못한 오류 처리
        return jsonify({"error": "Internal server error"}), 500

# abort(400, "...")를 바로 쓰면 Flask가 즉시 HTTP 응답을 반환해 주기는 하지만, 그 전에 필요한 DB 세션 롤백이나 공통 후속 처리(예: 로깅)를 놓칠 수 있습니다.
# 반면 raise ValueError("...")로 예외를 던지면, try/except ValueError 블록 안에서 DB 롤백이나 추가 작업을 일괄 처리한 뒤에 일관된 JSON 응답(400)을 반환할 수 있습니다.
# 그래서 abort로 잡았던 예외들을 try/except로 다시 잡았습니다