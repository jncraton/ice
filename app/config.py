""" Configuration file for Flask App. """


class Config:
    DATABASE_PATH = "db/ice-database.db"
    TESTING = False


class TestConfig(Config):
    DATABASE_PATH = ":memory:"
    TESTING = True
