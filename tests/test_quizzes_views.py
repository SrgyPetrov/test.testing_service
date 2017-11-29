import pytest

from django.urls import reverse


def test_quizzes_list(admin_client):
    response = admin_client.get(reverse('quizzes_list'))
    assert response.status_code == 200
    assert response.templates[0].name == 'quizzes/quiz_list.html'
    assert len(response.context[0]['object_list']) == 5
    assert response.context[0]['is_paginated']
    assert response.context[0]['paginator'].count == 7


def test_quizzes_list_answered(admin_client):
    url = reverse('quizzes_list')
    response = admin_client.get(url + '?page=1')
    assert response.context[0]['object_list'][0].answered_count == 0
    assert response.context[0]['object_list'][1].answered_count == 3
    response = admin_client.get(url + '?page=2')
    assert response.context[0]['object_list'][0].answered_count == 1
    assert response.context[0]['object_list'][1].answered_count == 0


def test_quizzes_list_anonimous(client):
    url = reverse('quizzes_list')
    redirect_url = '{}?next={}'.format(reverse('login'), url)
    response = client.get(url, follow=True)
    assert response.redirect_chain == [(redirect_url, 302)]
    assert response.status_code == 200


def test_quizzes_result_anonimous(client):
    url = reverse('quizzes_result', args=[2])
    redirect_url = '{}?next={}'.format(reverse('login'), url)
    response = client.get(url, follow=True)
    assert response.redirect_chain == [(redirect_url, 302)]
    assert response.status_code == 200


@pytest.mark.parametrize("quiz_id", [1, 6])
def test_quizzes_result_not_completed(admin_client, quiz_id):
    url = reverse('quizzes_result', args=[quiz_id])
    redirect_url = reverse('quizzes_detail', args=[quiz_id])
    response = admin_client.get(url, follow=True)
    assert response.redirect_chain == [(redirect_url, 302)]
    assert response.status_code == 200


def test_quizzes_result(admin_client):
    url = reverse('quizzes_result', args=[2])
    response = admin_client.get(url)
    assert response.status_code == 200
    assert response.templates[0].name == 'quizzes/quiz_detail.html'
    assert response.context[0]['object'].pk == 2
    assert response.context[0]['valid_count'] == 3
    assert response.context[0]['invalid_count'] == 0
    assert response.context[0]['percent'] == 100


def test_quizzes_detail_anonimous(client):
    url = reverse('quizzes_detail', args=[1])
    redirect_url = '{}?next={}'.format(reverse('login'), url)
    response = client.get(url, follow=True)
    assert response.redirect_chain == [(redirect_url, 302)]
    assert response.status_code == 200


def test_quizzes_detail_completed(admin_client):
    url = reverse('quizzes_detail', args=[2])
    redirect_url = reverse('quizzes_result', args=[2])
    response = admin_client.get(url, follow=True)
    assert response.redirect_chain == [(redirect_url, 302)]
    assert response.status_code == 200


def test_quizzes_detail(admin_client):
    url = reverse('quizzes_detail', args=[6])
    response = admin_client.get(url)
    assert response.status_code == 200
    assert response.templates[0].name == 'quizzes/quiz_question.html'
    assert response.context[0]['object'].pk == 7
    assert response.context[0]['question_number'] == 2
    assert response.context[0]['questions_count'] == 2
    assert not response.context[0]['form'].errors
    answers = response.context[0]['form'].fields['answers']
    assert len(answers.queryset.all()) == 2


def test_quizzes_detail_valid(admin_client, admin_user):
    response = admin_client.post(
        reverse('quizzes_detail', args=[1]),
        {'answers': ['46', '47', '48']},
        follow=True
    )
    assert response.redirect_chain == [
        (reverse('quizzes_detail', args=[1]), 302)
    ]
    assert admin_user.answers.filter(pk__in=[46, 47, 48]).count() == 3


def test_quizzes_detail_valid_finish(admin_client, admin_user):
    url = reverse('quizzes_detail', args=[6])
    response = admin_client.post(url, {'answers': ['17', '18']}, follow=True)
    assert response.redirect_chain == [
        (reverse('quizzes_detail', args=[6]), 302),
        (reverse('quizzes_result', args=[6]), 302)
    ]
    assert admin_user.answers.filter(pk__in=[17, 18]).count() == 2


def test_quizzes_detail_invalid(admin_client, admin_user):
    response = admin_client.post(
        reverse('quizzes_detail', args=[1]),
        {'answers': ['17', '18']}
    )
    assert response.context[0]['object'].pk == 20
    assert response.context[0]['form'].errors
    assert admin_user.answers.count() == 4
