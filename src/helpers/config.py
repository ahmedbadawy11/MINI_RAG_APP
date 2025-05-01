from pydantic_settings import BaseSettings, SettingsConfigDict 

import os
from dotenv import load_dotenv

# Manually load the .env file from the src directory
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

class settings(BaseSettings):

    APP_NAME:str
    APP_VERSION:str
    FILE_ALLOWED_TYPES:  list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE :int

    class config:
        env_file=".env"


def get_setting():
    settings_instance = settings()
    return settings_instance