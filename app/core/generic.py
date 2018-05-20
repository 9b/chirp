"""Generic calls within the application."""
from . import core
from .. import mongo, logger, celery
from flask import (
    render_template, redirect, url_for, jsonify, request, Response
)
from flask_login import login_required, current_user
from flask import current_app as app
from .forms import AccountSettingsForm, ChangePasswordForm, AdminForm
from ..utils.helpers import paranoid_clean
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash


@core.route('/')
@login_required
def root():
    """Render the index page."""
    logger.debug("User: %s" % (current_user.get_id()))
    users = mongo.db[app.config['USERS_COLLECTION']]
    user = users.find_one({'username': current_user.get_id()})
    monitors = mongo.db[app.config['MONITORS_COLLECTION']]
    results = list(monitors.find({'username': current_user.get_id()}))
    results.sort(key=lambda x: x['checked'], reverse=True)
    return render_template('index.html', name=user.get('first_name'),
                           monitors=results)


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
    if current_user.is_admin():
        g = mongo.db[app.config['GLOBAL_COLLECTION']]
        data = g.find_one(dict(), {'_id': 0})
        user['admin'] = data
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


@core.route('/admin/settings', methods=['POST'])
@login_required
def admin_save_settings():
    """Save settings for the admin accounts."""
    form = AdminForm(request.form)
    if not form.validate():
        errors = ','.join([value[0] for value in form.errors.values()])
        return jsonify({'errors': errors})

    c = mongo.db[app.config['GLOBAL_COLLECTION']]
    c.remove(dict())
    item = {'email': form.email.data, 'password': form.password.data}
    c.insert(item)
    return redirect(url_for('core.settings'))
