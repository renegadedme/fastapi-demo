from pydantic import BaseSettings
from paths import ENV_PATH
###from app.paths import ENV_PATH

#setting environment variables
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ENV_PATH   #specifies the file path of the env file

settings = Settings()

