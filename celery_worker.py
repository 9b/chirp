"""Run the Celery jobs."""
import os
from app import celery, create_app
import app.tasks

flask_app = create_app(os.getenv('FLASK_CONFIG') or 'default')
flask_app.app_context().push()