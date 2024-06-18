from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
  APP_NAME: str = 'Gpodder Clone'
  APP_VERSION: str = '0.0.1'
  APP_DESCRIPTION: str = 'An app that mimics gpodder.net'
  DB_URL:str = f'sqlite:///{str(os.getenv('DB_URL'))}'
  SECRET_KEY: str =  str(os.getenv('SECRET_KEY'))
  ALGORITHM:str = "HS256"

def get_settings():
  return Settings()
