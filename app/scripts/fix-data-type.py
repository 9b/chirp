"""Correct a bug in the data format for monitors."""
from bson.objectid import ObjectId

def mongo_connect(host, port, database, collection):
    """Connect to a mongo instance."""
    from pymongo import MongoClient
    return MongoClient(host, port)[database][collection]


def main():
    """."""
    db = mongo_connect('localhost', 27017, 'chirp', 'monitors')
    for item in db.find(dict()):
        metadata = item['metadata'][0]
        db.update({'_id': ObjectId(item['_id'])}, {'$set': {'metadata': metadata}})

if __name__ == "__main__":
    main()