class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@/muroran?unix_socket=/cloudsql/{cloud_sql_instance_name}'.format(
        **{
            'user': 'root',
            'password': 'root',
            'cloud_sql_instance_name': 'shimz-iur-dev-262123:asia-northeast1:muroran',
            # 'host': '35.221.112.87',
            # 'port': '3306'
        })
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Production configurations
    """


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
