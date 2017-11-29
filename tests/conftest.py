import pytest
from contextlib import contextmanager
from django.core.management import call_command
from django.db import connection
from django.test.utils import CaptureQueriesContext


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = ['quizzes.json', 'users.json']
        call_command('loaddata', *fixtures)


@pytest.fixture(scope='function')
def django_assert_num_queries():

    @contextmanager
    def _assert_num_queries(num):
        with CaptureQueriesContext(connection) as context:
            yield
            if num != len(context):
                msg = "Expected to perform %s queries but %s were done" % (
                    num, len(context))
                pytest.fail(msg)
    return _assert_num_queries
