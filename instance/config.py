import os


class Config(object):
    """
    Parent configuration class
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class StagingConfig(Config):
    """
    Staging configuration
    """
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Configuration for development
    """
    DEBUG = True


class TestingConfig(DevelopmentConfig):
    """
    Test configuration (with separate db)
    """
    TESTING = True
    SQLALCHEMY_DATABSAE_URI = 'postgresql://localhost/test'


class ProductionConfig(Config):
    """
    Prod configuration
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
