""" Configuration file for Flask App. """

class Config:
    DATABASE_PATH = "../app/db/ice-database.db"
    TESTING = False


class TestConfig(Config):
    DATABASE_PATH = ":memory:"
    TESTING = True
