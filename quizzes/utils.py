from .models import Question


def get_user_current_question(user, quiz_id):
    user_answers = user.answers.filter(question__quiz_id=quiz_id)
    qs = Question.objects.filter(quiz_id=quiz_id)
    qs = qs.exclude(answers__in=user_answers)
    return qs.first()


def get_question_number(quiz_id, question_id):
    qs = Question.objects.filter(quiz_id=quiz_id)
    pks = list(qs.values_list('pk', flat=True))
    return {
        'questions_count': len(pks),
        'question_number': pks.index(question_id) + 1
    }


def get_user_results(user, quiz_id):
    answers = user.answers.filter(question__quiz_id=quiz_id)
    valid_count = answers.valid().count()
    invalid_count = answers.invalid().count()
    percent = valid_count * 100 / (valid_count + invalid_count)
    return {
        'valid_count': valid_count,
        'invalid_count': invalid_count,
        'percent': round(percent, 2)
    }
