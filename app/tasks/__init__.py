"""Tasks related to celery."""
from .. import mongo, logger
from bson.objectid import ObjectId
from flask import current_app as app
import celery
import feedparser
import hashlib
import json
import justext
import nltk
import sys
from app.utils.helpers import (
    now_time, strip_google, derive_source, get_page_content, get_tokens,
    cleaned_tokens, get_sentiment
)


@celery.task(name="heartbeat")
def heartbeat():
    """Look alive."""
    logger.debug("I am the beat.")


def is_found(uuid):
    """Check to see if we already processed the article."""
    articles = mongo.db[app.config['ARTICLES_COLLECTION']]
    hit = articles.find_one({'uuid': uuid})
    if not hit:
        return False
    return hit


def get_article(item, source, reprocess=False):
    """Take the initial set of listings and enrich the content."""
    article = dict()
    encoded = item.get('link').encode('utf-8')
    article['uuid'] = hashlib.sha256(encoded).hexdigest()
    processed = is_found(article['uuid'])
    if processed and not reprocess:
        return {'article': processed, 'from_store': True}
    article['title'] = item.get('title', None)
    href = item.get('link', None)
    article['href'] = strip_google(href)
    article['source'] = derive_source(article['href'])
    article['collected'] = now_time()
    article['published'] = item.get('published', None)
    article['summary'] = item.get('summary', None)

    page_content = get_page_content(article['href'])
    if not page_content:
        logger.debug("No content found: %s" % article['href'])
        return {'article': None, 'from_store': True}
    paragraphs = justext.justext(page_content,
                                 justext.get_stoplist("English"),
                                 no_headings=True,
                                 max_heading_distance=150,
                                 length_high=140,
                                 max_link_density=0.4,
                                 stopwords_low=0.2,
                                 stopwords_high=0.3)
    text_content = list()
    for paragraph in paragraphs:
        if paragraph.is_boilerplate:
            continue
        text_content.append(paragraph.text)
    text_content = '\n'.join(text_content)
    tokens = get_tokens(text_content)

    article['word_count'] = len(tokens)
    article['read_time'] = round(float(article['word_count'])/250, 2)
    clean = cleaned_tokens(tokens)
    article['tokens'] = [{t[0]:t[1]}
                         for t in nltk.FreqDist(clean).most_common(100)]
    article['tags'] = [list(x.keys())[0] for x in article['tokens'][0:7]]
    article['sentiment'] = get_sentiment(text_content)
    article['feed_source'] = source.replace('www.google.com', 'google.com')
    articles = mongo.db[app.config['ARTICLES_COLLECTION']]
    if not reprocess:
        try:
            articles.insert(article)
        except:
            pass
    else:
        if not processed:
            try:
                articles.insert(article)
            except:
                pass
        articles.update({'_id': ObjectId(processed['_id'])}, {'$set': article})
    return {'article': article, 'from_store': False}


@celery.task(name="process_all_rss")
def process_all_rss(reprocess=False):
    """Gather all RSS feeds and articles, then process."""
    sources = list()
    monitors = mongo.db[app.config['MONITORS_COLLECTION']]
    for item in monitors.find(dict()):
        sources.append(item['metadata'].get('rss_link'))

    contents = [feedparser.parse(x) for x in sources]
    for source in contents:
        for idx, item in enumerate(source.get('entries')):
            response = get_article(item, source['href'], reprocess)
            if response['from_store'] or reprocess:
                continue
            clean_link = response['article']['feed_source']
            monitors.update({'metadata.rss_link': clean_link},
                            {'$inc': {'hits': 1}})
            monitors.update({'metadata.rss_link': clean_link},
                            {'$set': {'checked': now_time()}})
