from app.models import Question

def get_all_questions():
    return [q.to_dict() for q in Question.query.all()]
