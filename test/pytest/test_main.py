"""
Contains the functional tests for the main blueprint.
"""
from tests.pytest_tests.conftest import login


def test_index_page_valid(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' home page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_index_content(test_client):
    """
        GIVEN a Flask application
        WHEN the '/' home page is requested
        THEN check the response contains "Welcome!"
        """
    response = test_client.get('/')
    assert b'Welcome' in response.data


def test_index_returns_name_when_username_given(test_client, user):
    """
        GIVEN a Flask application
        WHEN the '/' home page is requested with a logged in user
        THEN check the response contains "Welcome <name>"

    """
    name = user.name
    response = test_client.get('/{}'.format(name))
    assert b'Welcome Another Person' in response.data


def test_profile_displayed_when_user_logged_in(test_client, user):
    """Tests a view that requires authentication"""
    login(test_client, password=user.password, username=user.email)
    assert current_user.is_authenticated
    response = test_client.get('/view_profile')
    assert response.status_code == 200
    assert b'Welcome Another Person' in response.data