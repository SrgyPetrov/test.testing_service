from itertools import groupby
from operator import attrgetter

from users.models import UserAnswer

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
    answers = answers.values_list('is_valid', flat=True)
    return get_results_from_answers(answers)


def get_user_stats(user):
    stats = {}
    answers = user.answers.all().order_by('question__quiz_id')
    answers = answers.select_related('question__quiz')
    for quiz, items in groupby(answers, attrgetter('question.quiz')):
        stats[quiz] = get_results_from_answers(i.is_valid for i in items)
    return stats


def get_results_from_answers(answers):
    answers = list(answers)
    valid_count = answers.count(True)
    invalid_count = answers.count(False)
    if valid_count or invalid_count:
        percent = valid_count * 100 / (valid_count + invalid_count)
    else:
        percent = 0.0
    return {
        'valid_count': valid_count,
        'invalid_count': invalid_count,
        'percent': round(percent, 2)
    }


def create_user_answers(user, answers):
    UserAnswer.objects.bulk_create(
        UserAnswer(user=user, answer=answer) for answer in answers
    )
