import os
from datetime import datetime, timezone

from dcmain.appstrings import ccl, lcl, ucl


class Config:
    """
    GENEARL CONFIG ITEMS
    """
    DEFAULT_TIMEZONE = "Africa/Lagos"
    # ``DEFAULT_TIMEZONE_RETURN``
    # is whats returned by dt.tzname()
    # after creating dt with Africa/Lagos
    DEFAULT_TIMEZONE_RETURN = ucl.WAT
    SECRET_KEY = os.environ.get(ucl.SECRET_KEY)
    CONFIG_TYPE = None  # updated in application factory
    COMMIT_HASH = datetime.now(tz=timezone.utc).isoformat()
    TRADEPALLY_LOCALHOST_API_AUTH_TOKEN = f"Bearer {os.environ.get(ucl.TRADEPALLY_LOCALHOST_API_AUTH_TOKEN)}"
    TRADEPALLY_PRODUCTION_API_AUTH_TOKEN = f"Bearer {os.environ.get(ucl.TRADEPALLY_PRODUCTION_API_AUTH_TOKEN)}"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT_ENV = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    TESTING_ENV = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "test.localhost:5000"


class ProductionConfig(Config):
    PRODUCTION_ENV = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config_classes = {
    lcl.testing: TestingConfig,
    lcl.default: DevelopmentConfig,
    lcl.production: ProductionConfig,
    lcl.development: DevelopmentConfig,
}
