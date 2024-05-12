import pymongo

mongo_url = 'mongodb://xxx'
def connMongo():
    client = pymongo.MongoClient(mongo_url)
    db = client['bookstore']
    print(client.list_database_names())
    print(db.list_collection_names())

    users_col = db['users']
    print(users_col.find_one())
    return db


if __name__ == '__main__':
    connMongo()