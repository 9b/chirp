import operator
from copy import deepcopy
from flask import (
    render_template, redirect, url_for, jsonify, request
)
from flask import current_app as app
from flask_login import login_required, current_user
from . import core
from .. import mongo, logger, celery
from ..utils.helpers import paranoid_clean, offset_time_past, load_time
from collections import OrderedDict


@core.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard page."""
    logger.debug("User: %s" % (current_user.get_id()))
    users = mongo.db[app.config['USERS_COLLECTION']]
    user = users.find_one({'username': current_user.get_id()})
    monitors = mongo.db[app.config['MONITORS_COLLECTION']]
    results = list(monitors.find({'username': current_user.get_id()}))
    results.sort(key=lambda x: x['checked'], reverse=True)
    return render_template('dashboard.html', name=user.get('first_name'),
                           monitors=results)


@core.route('/data/article-by-day-30', methods=['GET'])
@login_required
def dashboard_article_by_day_30():
    """Dashboard to show content ingestion counts in the past 30 days."""
    response = OrderedDict({'Sun': 0, 'Mon': 0, 'Tue': 0, 'Wed': 0,
                            'Thu': 0, 'Fri': 0, 'Sat': 0})
    int2day = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3:
               'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    past_30 = offset_time_past(30, str=True)
    articles = mongo.db[app.config['ARTICLES_COLLECTION']]
    results = articles.find({'collected': {'$gt': past_30}}, {'_id': 0})
    for result in results:
        t = load_time(result['collected'])
        response[int2day[t.weekday()]] += 1
    data = [x for x in response.values()]
    return jsonify(data)


@core.route('/data/count-by-monitor-by-day-30', methods=['GET'])
@login_required
def dashboard_monitor_heatmap():
    """."""
    # [0, 0, 10] [monitor, day, count]
    past_30 = offset_time_past(30, str=True)
    monitors = mongo.db[app.config['MONITORS_COLLECTION']]
    articles = mongo.db[app.config['ARTICLES_COLLECTION']]
    sources = articles.distinct('feed_source',
                                {'collected': {'$gt': past_30}})
    terms = list()
    for source in sources:
        monitor = monitors.find_one({'metadata.rss_link': source}, {'_id': 0})
        terms.append(monitor.get('term'))
    days = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    stats = {term: deepcopy(days) for term in terms}
    results = articles.find({'collected': {'$gt': past_30}}, {'_id': 0})
    for result in results:
        t = load_time(result['collected'])
        monitor = monitors.find_one({'metadata.rss_link': result['feed_source']}, {'_id': 0})
        stats[monitor['term']][t.weekday()] += 1
    count = 0
    data = {'series': list(), 'data': list()}
    for key, value in stats.items():
        data['series'].append(key)
        for k, v in value.items():
            data['data'].append([count, k, v])
        count += 1
    return jsonify(data)


@core.route('/data/article-tag-cloud', methods=['GET'])
@login_required
def dashboard_content_article_tag_cloud():
    """Dashboard to show the top 25 article tags."""
    tag_stats = dict()
    past_30 = offset_time_past(30, str=True)
    articles = mongo.db[app.config['ARTICLES_COLLECTION']]
    results = articles.find({'collected': {'$gt': past_30}}, {'_id': 0})
    for result in results:
        for tag in result.get('tags', list()):
            tag_stats[tag] = tag_stats.get(tag, 0) + 1
    tags_sorted = sorted(tag_stats.items(), key=operator.itemgetter(1),
                         reverse=True)[:50]
    data = list()
    for item in tags_sorted:
        data.append({'name': item[0], 'weight': item[1]})
    return jsonify(data)


@core.route('/data/article-sources', methods=['GET'])
@login_required
def dashboard_article_sources():
    """Dashboard to article source distribution."""
    sources = dict()
    past_30 = offset_time_past(30, str=True)
    articles = mongo.db[app.config['ARTICLES_COLLECTION']]
    results = articles.find({'collected': {'$gt': past_30}}, {'_id': 0})
    for result in results:
        sources[result['source']] = sources.get(result['source'], 0) + 1
    sources = sorted(sources.items(), key=operator.itemgetter(1), reverse=True)
    data = sources[:10]
    return jsonify(data)
