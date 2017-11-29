import pytest

from django.urls import reverse


def test_login(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert response.templates[0].name == 'users/login.html'
    assert not response.context[0]['user'].is_authenticated
    assert not response.context[0]['form'].errors


@pytest.mark.django_db
def test_login_valid(client):
    response = client.post(
        reverse('login'),
        {'username': 'admin', 'password': 'qwerty'},
        follow=True
    )
    assert response.redirect_chain == [('/', 302)]
    assert response.status_code == 200
    assert response.context[0]['user'].is_authenticated


@pytest.mark.django_db
def test_login_invalid(client):
    response = client.post(
        reverse('login'),
        {'username': 'qwerty', 'password': 'admin'},
        follow=True
    )
    assert response.redirect_chain == []
    assert response.status_code == 200
    assert not response.context[0]['user'].is_authenticated
    assert response.context[0]['form'].errors


def test_signup(client):
    response = client.get(reverse('signup'))
    assert response.status_code == 200
    assert response.templates[0].name == 'users/signup.html'
    assert not response.context[0]['user'].is_authenticated
    assert not response.context[0]['form'].errors


@pytest.mark.django_db
def test_signup_valid(client):
    response = client.post(
        reverse('signup'),
        {'username': 'user', 'password1': 'qwerty', 'password2': 'qwerty'},
        follow=True
    )
    assert response.redirect_chain == [(reverse('quizzes_list'), 302)]
    assert response.status_code == 200
    assert response.context[0]['user'].is_authenticated


@pytest.mark.django_db
def test_signup_invalid(client):
    response = client.post(
        reverse('signup'),
        {'username': 'user', 'password1': 'qwerty', 'password2': 'qwe'},
        follow=True
    )
    assert response.redirect_chain == []
    assert response.status_code == 200
    assert not response.context[0]['user'].is_authenticated
    assert response.context[0]['form'].errors


def test_logout(admin_client):
    response = admin_client.get(reverse('logout'), follow=True)
    assert response.redirect_chain == [(reverse('login'), 302)]
    assert response.status_code == 200
    assert not response.context[0]['user'].is_authenticated
