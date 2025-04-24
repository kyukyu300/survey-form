from app.models import Question

# 모든 질문 조회
def get_all_questions():
    return [q.to_dict() for q in Question.query.all()]

# 질문 하나씩 조회
def get_question_by_id(question_id):
    question = Question.query.get(question_id)
    if question:
        return question.to_dict() 
    else:
        None
