import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# Environment variables
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")
url = os.getenv("URL_DB", "localhost:5432")


class Config(object):
    # DataBase Settings
    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{url}/document"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
