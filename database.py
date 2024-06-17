from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from settings import get_settings


def get_db():
  try:
    settings = get_settings()
    cluster = MongoClient(settings.DB_URI, server_api=ServerApi('1'))
    cluster.admin.command('ping')
    collection = cluster['python_opml_sync']
    return collection["Users Podcasts"]
  except ConnectionFailure as e:
    print(e)
