from os import environ
from pathlib import Path
from dotenv import load_dotenv

flask_env = environ.get("FLASK_ENV", "development")
env_file_path = Path(f".env.{flask_env}")
load_dotenv(dotenv_path=env_file_path, verbose=True)

FLASK_ENV = flask_env
FLASK_APP = "server:app"
DEBUG = 1 if flask_env == "development" else 0

db_name = environ.get("DATABASE_NAME")
SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:@localhost:5432/{db_name}"
SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", 0)
