from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
  APP_NAME: str = 'podcast sync service'
  APP_VERSION: str = '0.0.1'
  APP_DESCRIPTION: str = 'An app to sync your podcasts opml files'
  DB_URI:str = str(os.getenv('DB_URI'))
  SECRET_KEY: str =  str(os.getenv('SECRET_KEY'))
  ALGORITHM:str = "HS256"

def get_settings():
  return Settings()