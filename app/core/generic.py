"""Generic calls within the application."""
from . import core
from .. import mongo, logger, celery
from flask import (
    render_template, redirect, url_for, jsonify, request, Response
)
from flask_login import login_required, current_user
from flask import current_app as app
from .forms import AccountSettingsForm, ChangePasswordForm
from ..utils.helpers import paranoid_clean
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash


@core.route('/')
@login_required
def root():
    """Render the index page."""
    logger.debug("User: %s" % (current_user.get_id()))
    c = mongo.db[app.config['USERS_COLLECTION']]
    user = c.find_one({'username': current_user.get_id()})
    return render_template('index.html', name=user.get('first_name'))


@core.route('/async-test')
@login_required
def heartbeat_example():
    """Run an async job in the background."""
    logger.debug("Executing the heartbeat task and returning")
    celery.send_task('heartbeat')
    return render_template('index.html', name="HEARTBEAT")


@core.route('/settings')
@login_required
def settings():
    """Render the settings page."""
    c = mongo.db[app.config['USERS_COLLECTION']]
    user = c.find_one({'username': current_user.get_id()})
    if not user:
        return render_template()
    user['id'] = str(user['_id'])
    user.pop('_id', None)
    return render_template('settings.html', user=user)


@core.route('/account/settings/update', methods=['POST'])
@login_required
def update_account():
    """Update account settings."""
    logger.debug("User account settings update")
    form = AccountSettingsForm(request.form)
    if form.validate():
        if 'user_id' not in request.form:
            return jsonify({'success': False,
                            'error': 'ID not found in edit!'})
        logger.debug("Form validated")
        edit_id = paranoid_clean(request.form.get('user_id'))
        c = mongo.db[app.config['USERS_COLLECTION']]
        item = {'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'email': form.email.data}
        c.update({'_id': ObjectId(edit_id)}, {'$set': item})
        logger.debug("User account updated")
        return redirect(url_for('core.settings'))
    errors = ','.join([value[0] for value in form.errors.values()])
    return jsonify({'errors': errors})


@core.route('/account/settings/change-password', methods=['POST'])
@login_required
def account_change_password():
    """Update account password."""
    form = ChangePasswordForm(request.form)
    if form.validate():
        if 'user_id' not in request.form:
            return jsonify({'success': False,
                            'error': 'ID not found in edit!'})
        edit_id = paranoid_clean(request.form.get('user_id'))
        c = mongo.db[app.config['USERS_COLLECTION']]
        item = {'password': generate_password_hash(form.password.data)}
        c.update({'_id': ObjectId(edit_id)}, {'$set': item})
        return redirect(url_for('core.settings'))
    errors = ','.join([value[0] for value in form.errors.values()])
    return jsonify({'errors': errors})
