from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def page_not_found(e):
    return render_template('errors/404.html'), 404


def internal_server_error(e):
    return render_template('errors/500.html'), 500


def create_app(config_class=None):
    """
    Creates an application instance to run
    :return: A Flask object
    """
    app = Flask(__name__)

    # Configure app wth the settings from config.py
    app.config.from_object(config_class)

    # Initialise plugins
    db.init_app(app)
    login_manager.init_app(app)

    from cscourses.models import Teacher, Student, Course, Grade
    with app.app_context():
        db.drop_all()
        db.create_all()

    # Register error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    # Register Blueprints
    from cscourses.main.routes import bp_main
    app.register_blueprint(bp_main)

    from cscourses.auth.routes import bp_auth
    app.register_blueprint(bp_auth)

    return app
