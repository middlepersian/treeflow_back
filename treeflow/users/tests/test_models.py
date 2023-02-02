import pytest

from treeflow.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5