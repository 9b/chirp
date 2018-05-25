from . import core
from .. import mongo, celery, logger
from .forms import MonitorForm
from bson.objectid import ObjectId
from flask import (
    render_template, redirect, url_for, jsonify, request
)
from ..utils.helpers import now_time, paranoid_clean
from flask import current_app as app
from flask_login import login_required, current_user
from google_alerts import GoogleAlerts
import hashlib
import html


@core.route('/monitors/add-monitor', methods=['POST'])
@login_required
def add_monitor():
    """Render the index page."""
    form = MonitorForm(request.form)
    print(request.form)
    if not form.validate():
        errors = ','.join([value[0] for value in form.errors.values()])
        return jsonify({'errors': errors})

    g = mongo.db[app.config['GLOBAL_COLLECTION']]
    gdata = g.find_one(dict(), {'_id': 0})
    ga = GoogleAlerts(gdata['email'], gdata['password'])
    ga.authenticate()
    options = {'delivery': 'RSS', 'exact': form.type.data == 'Exact'}
    response = ga.create(form.term.data, options)
    if len(response) > 0:
        response = response[0]
    monitors = mongo.db[app.config['MONITORS_COLLECTION']]
    to_hash = form.type.data.encode('utf-8') + form.term.data.encode('utf-8')
    item = {'term': form.term.data,
            'exact': form.type.data == 'Exact',
            'tags': form.tags.data.split(','),
            'category': form.category.data.lower(),
            'username': current_user.get_id(),
            'created': now_time(),
            'active': True,
            'metadata': response,
            'hits': 0,
            'hashed': hashlib.sha256(to_hash).hexdigest(),
            'checked': now_time()}
    _id = monitors.insert(item)
    return redirect(url_for('core.root'))


@core.route('/monitors', methods=['GET'])
@login_required
def get_monitor_details():
    """Render the index page."""
    monitor_id = paranoid_clean(request.args.get('id'))
    monitors = mongo.db[app.config['MONITORS_COLLECTION']]
    monitor = monitors.find_one({'hashed': monitor_id}, {'_id': 0})
    if not monitor:
        return jsonify({'success': False, 'error': 'Monitor was not found.'})
    articles = mongo.db[app.config['ARTICLES_COLLECTION']]
    link = monitor['metadata']['rss_link']
    articles = list(articles.find({'feed_source': link}, {'_id': 0}))
    for idx, item in enumerate(articles):
        articles[idx]['title'] = html.unescape(item['title'])
        articles[idx]['date'] = item['collected'][:10]
    articles.sort(key=lambda x: x['collected'], reverse=True)
    return jsonify({'success': True, 'monitor': monitor, 'articles': articles})


@core.route('/monitors/list', methods=['GET'])
@login_required
def get_monitors():
    """Render the index page."""
    monitors = mongo.db[app.config['MONITORS_COLLECTION']]
    results = monitors.find(dict(), {'_id': 0})
    results = [x for x in results]
    results.sort(key=lambda x: x['hits'], reverse=True)
    return render_template('monitors.html', monitors=results)


@core.route('/async-rss')
@login_required
def trigger_rss():
    """Run an async job in the background."""
    logger.debug("Executing the heartbeat task and returning")
    celery.send_task('process_all_rss', kwargs={'reprocess': False})
    return render_template('index.html', name="HEARTBEAT")


@core.route('/async-reprocess')
@login_required
def reprocess_all_feeds():
    """Run an async job in the background."""
    logger.debug("Executing the heartbeat task and returning")
    celery.send_task('process_all_rss', kwargs={'reprocess': True})
    return render_template('index.html', name="HEARTBEAT")
