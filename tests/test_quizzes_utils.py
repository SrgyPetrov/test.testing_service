import pytest

from quizzes.models import Quiz, Answer
from quizzes import utils


@pytest.mark.parametrize("quiz_id,question_id", [
    (1, 20), (2, None), (6, 7)
])
def test_get_user_current_question(admin_user, quiz_id, question_id):
    question = utils.get_user_current_question(admin_user, quiz_id)
    if question_id is None:
        assert question is None
    else:
        assert question.pk == question_id


@pytest.mark.django_db
@pytest.mark.parametrize("quiz_id,question_id,count,number", [
    (1, 14, 7, 4), (1, 20, 7, 1), (3, 3, 1, 1), (6, 7, 2, 2)
])
def test_get_question_number(quiz_id, question_id, count, number):
    result = utils.get_question_number(quiz_id, question_id)
    assert result == {
        'questions_count': count,
        'question_number': number
    }


@pytest.mark.parametrize("answers,valid,invalid,percent", [
    ((True, False, True, False), 2, 2, 50.0),
    ((True, True, False), 2, 1, 66.67),
    ((False,), 0, 1, 0.0),
    ((True,), 1, 0, 100.0),
    ((), 0, 0, 0.0)
])
def test_get_results_from_answers(answers, valid, invalid, percent):
    result = utils.get_results_from_answers(answers)
    assert result == {
        'valid_count': valid,
        'invalid_count': invalid,
        'percent': percent
    }


@pytest.mark.parametrize("quiz_id,valid,invalid,percent", [
    (1, 0, 0, 0.0), (2, 3, 0, 100.0), (6, 0, 1, 0.0)
])
def test_get_user_results(admin_user, quiz_id, valid, invalid, percent):
    result = utils.get_user_results(admin_user, quiz_id)
    assert result == {
        'valid_count': valid,
        'invalid_count': invalid,
        'percent': percent
    }


def test_get_user_stats(admin_user):
    result = utils.get_user_stats(admin_user)
    assert result == {
        Quiz.objects.get(pk=2): {
            'valid_count': 3,
            'invalid_count': 0,
            'percent': 100.0
        },
        Quiz.objects.get(pk=6): {
            'valid_count': 0,
            'invalid_count': 1,
            'percent': 0.0
        }
    }


def test_create_user_answers(admin_user, django_assert_num_queries):
    answers = list(Answer.objects.filter(pk__in=[20, 21, 22, 23]))
    with django_assert_num_queries(1):
        utils.create_user_answers(admin_user, answers)
    assert admin_user.answers.count() == 8
