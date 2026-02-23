import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Database:
    URI = os.environ["DATABASE_URL"]
    DATABASE = None

    def __init__(self):
        self._client = MongoClient(self.URI, maxPoolSize=1)
        self.DATABASE = self._client.stocks

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def close(self, commit=True):
        self._client.close()

    def drop(self, collection):
        self.DATABASE[collection].drop()

    def fetchall(self, collection, query={}):
        return self.DATABASE[collection].find(query, {'_id': False})

    def fetchone(self, collection, query={}):
        return self.DATABASE[collection].find_one(query, {'_id': False})
    
    def insert(self, collection, data):
        self.DATABASE[collection].insert_one(data)

    def insert_many(self, collection, data):
        self.DATABASE[collection].insert_many(data)

    def update(self, collection, data, query={}):
        try:
            new_values = { "$set": data }
            self.DATABASE[collection].update_one(query, new_values)
        except Exception as e:
            raise e

    def get_categories(self):
        try:
            result = self.fetchall("category")
            docs = []

            for document in result:
                docs.append(document)

            result.close()

            return docs
        except Exception as e:
            raise e

    def get_stocks_by_category(self, category=None):
        try:
            filter = {}
            
            if category is not None:
                filter["category"] = category

            result = self.fetchall("stock", filter)
            docs = []

            for document in result:
                docs.append(document)

            result.close()
            
            return docs
        except Exception as e:
            print(e)
            raise e

    def insert_stock_data(self, stocks_data):
        result = None

        try:
            self.drop("stock")
            result = self.insert_many("stock", stocks_data)

            return result
        except Exception as e:
            print(e)
        finally:
            if result:
                result.close()

    def add_category(self, data):
        result = None

        try:
            result = self.insert("category", data)

            return result
        except Exception as e:
            raise e
        finally:
            if result:
                result.close()

    def get_last_update(self):
        try:
            return self.fetchone("stats")
        except Exception as e:
            print(e)
            raise e