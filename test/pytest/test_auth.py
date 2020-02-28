"""
Contains tests for the auth blueprint
"""
from tests.pytest_tests.conftest import login


def test_login_fails_with_invalid_username(test_client, app):
    with app.test_request_context():
        response = login(test_client, username="John", password='Fred')
        assert 'Invalid username or password' in response.get_data(as_text=True)
        # assert b'Invalid username or password' in response.data


def test_login_success_with_valid_user(test_client, user):
    """ Tests if the login form works when the user exists and details are valid """
    with test_client:
        response = test_client.post('/login/', data=dict(
            email=user.email,
            password=user.password
        ), follow_redirects=True)
    assert response.status_code == 200


def test_register_student_success(student_data, test_client):
    response = test_client.post('/signup/', data=dict(
        email=student_data['email'],
        password=student_data['password'],
        name=student_data['name'],
        title=student_data['title'],
        role=student_data['role'],
        uni_id=student_data['uni_id'],
        confirm=student_data['confirm']
    ), follow_redirects=True)
    assert response.status_code == 200
