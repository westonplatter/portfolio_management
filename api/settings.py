from os import environ
from pathlib import Path
from dotenv import dotenv_values

app_env = environ.get("ENV", "development")
env_file_path = Path(f".env.{app_env}")
configs = dotenv_values(env_file_path)

FLASK_ENV = app_env
FLASK_APP = "server:app"
DEBUG = 1 if app_env == "development" else 0

port = environ.get("POSTGRES_PORT", "5432")

print("--------------------")
print(f"port = {port}")
print("--------------------")

uri = configs.get("SQLALCHEMY_DATABASE_URI")
uri = uri.replace("5432", port)
SQLALCHEMY_DATABASE_URI = uri

SQLALCHEMY_TRACK_MODIFICATIONS = configs.get("SQLALCHEMY_TRACK_MODIFICATIONS", 0)
