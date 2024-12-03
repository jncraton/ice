""" Configuration file for Flask App. """


class Config:
    """
    Default configuration object

    Any configuration settings changed here will be applied in both testing and default situations
    """

    # pylint: disable=too-few-public-methods
    DATABASE_PATH = "db/ice-database.db"
    TESTING = False


class TestConfig(Config):
    """
    Testing configuration object

    Any configuration settings changed here will override settings from the default configuration
    object when running tests.
    """

    # pylint: disable=too-few-public-methods
    DATABASE_PATH = ":memory:"
    TESTING = True
