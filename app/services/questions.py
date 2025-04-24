from app.models import Question

def get_all_questions():
    return Question.query.all()