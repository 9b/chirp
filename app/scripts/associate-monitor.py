"""Associate the monitor with the article for quick reference."""
from bson.objectid import ObjectId


def mongo_connect(host, port, database, collection):
    """Connect to a mongo instance."""
    from pymongo import MongoClient
    return MongoClient(host, port)[database][collection]


def get_monitor_obj(link):
    """Get the monitor object by the RSS link."""
    monitors = mongo_connect('localhost', 27017, 'chirp', 'monitors')
    monitor = monitors.find_one({'metadata.rss_link': link}, {'_id': 0})
    return monitor


def main():
    """."""
    articles = mongo_connect('localhost', 27017, 'chirp', 'articles')
    monitors = mongo_connect('localhost', 27017, 'chirp', 'monitors')
    for item in articles.find(dict()):
        obj = get_monitor_obj(item['feed_source'])
        db.update({'_id': ObjectId(item['_id'])}, {'$set': {'monitor': obj}})


if __name__ == "__main__":
    main()
