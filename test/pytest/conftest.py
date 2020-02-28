"""Fixtures for the tests"""

import pytest
from flask_login import login_user, logout_user

from cscourses import create_app
from cscourses import db as _db


@pytest.yield_fixture(scope='session')
def app(request):
    """Create a test client to send requests to"""
    _app = create_app('config.TestConfig')
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def test_client(app):
    """ Exposes the Werkzeug test client for use in the tests. """
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function')
def user(test_client, db):
    """ Creates a student user. """
    from cscourses.models import Student
    user = Student(name='Another Person', email='anotherperson@gmail.com', user_type='student', student_ref='cs987654')
    user.set_password('cs987654')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='function', autouse=True)
def session(db):
    """ Rolls back database changes at the end of each test """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()


@pytest.fixture(scope='function')
def logged_in_user(app, request, user):
    """ Creates a logged in user and logs them out again when the test is complete using Flask-Login """
    with app.test_request_context():
        login_user(user)

    request.addfinalizer(logout_user)


@pytest.fixture(scope='function')
def student_data():
    """ Provides the details for a student. """
    student_data = {
        "name": "Fred Blogs",
        "title": None,
        "role": "Student",
        "uni_id": "cs123456",
        "email": "cs123456@ucl.ac.uk",
        "password": "test",
        "confirm": "test"
    }
    return student_data


@pytest.fixture(scope='function')
def teacher_data():
    """ Provides the details for a teacher. """
    teacher_data = {
        "name": "Jane Smith",
        "title": "Dr",
        "role": "Teacher",
        "uni_id": "ct123456",
        "email": "ct123456@ucl.ac.uk",
        "password": "test",
        "confirm": "test"
    }
    return teacher_data


# Helper functions ( not fixtures) from https://flask.palletsprojects.com/en/1.1.x/testing/
def login(client, username, password):
    return client.post('/login/', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout/', follow_redirects=True)
