# Refer to https://flask.palletsprojects.com/en/1.1.x/config/ for more information.
import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_DATABASE = os.environ["POSTGRES_DATABASE"]

    @property
    def DATABASE_URI(self):
        return "postgresql://%s:%s@%s:%s/%s" % (
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            str(self.POSTGRES_PORT),
            self.POSTGRES_DATABASE,
        )


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
