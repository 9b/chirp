"""
Initialize the application and import all the blueprints.

This file will initialize all of the global variables used within the rest of
the application. Anything needed for the app context will be done within the
`create_app` function and returned back to the caller handler.
"""
from .models.user import User
from celery import Celery
from celery.schedules import crontab
from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager
from flask_pymongo import PyMongo
import logging
import sys

APP_NAME = 'app-strap'

login_manager = LoginManager()
mongo = PyMongo()
celery = Celery(APP_NAME)

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)
shandler = logging.StreamHandler(sys.stdout)
fmt = '\033[1;32m%(levelname)-5s %(module)s:%(funcName)s():'
fmt += '%(lineno)d %(asctime)s\033[0m| %(message)s'
shandler.setFormatter(logging.Formatter(fmt))
logger.addHandler(shandler)


@login_manager.user_loader
def load_user(username):
    """Create a manager to reload sessions.

    :param username: Username of the logged in user
    :type username: str
    :returns: User
    """
    from flask import current_app as app
    c = mongo.db[app.config['USERS_COLLECTION']]
    u = c.find_one({"username": username})
    if not u:
        return None
    return User(u)


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to the login page."""
    return redirect(url_for('core.login'))


def server_error(e):
    """500 handler."""
    logger.error("500 triggered: %s" % (str(e)))
    return render_template("500.html")


def page_not_found(e):
    """404 handler."""
    logger.info("404 triggered: Path %s" % (request.path))
    return render_template("404.html")


def create_app(debug=False):
    """Create an application context with blueprints."""
    app = Flask(__name__, static_folder='./resources')
    app.config['SECRET_KEY'] = 'RYVl4Fg3n1JLDaxWyr1m'
    app.config['MONGO_DBNAME'] = 'app_strap'
    app.config['USERS_COLLECTION'] = 'accounts'
    login_manager.init_app(app)
    mongo.init_app(app)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379',
        CELERYBEAT_SCHEDULE={
            'heartbeat': {
                'task': 'heartbeat',
                'schedule': crontab(minute='*')
            }
        }
    )
    celery.conf.update(app.config)

    from .core import core as core_blueprint
    app.register_blueprint(core_blueprint)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    return app
