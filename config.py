import redis

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    # session加密密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # 决定是否追踪对象的修改，SQLAlchemy建议配置此变量，不然会有警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮箱服务器地址
    MAIL_SERVER = 'smtp.163.com'

    # 邮箱服务器端口
    MAIL_PORT = 994

    # 邮箱使用SSL
    MAIL_USE_SSL = True

    # 邮箱地址
    MAIL_USERNAME = "xcc_mail@163.com"

    # 邮箱授权码
    MAIL_PASSWORD = "VHGQMYFJNNPJQYSA"

    # 默认发送方：用户名+地址
    MAIL_DEFAULT_SENDER = ('徐聪聪', "xcc_mail@163.com")

    # 默认管理员邮箱
    FLASKY_ADMIN = "1138084278@qq.com"

    # 默认邮件主题
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'

    # 每页显示评论数
    FLASKY_POSTS_PER_PAGE = 10

    # 每页显示关注者数
    FLASKY_FOLLOWERS_PER_PAGE = 50

    FLASKY_COMMENTS_PER_PAGE = 15

    REDIS_CLIENT = redis.StrictRedis(host='192.168.137.136', port=6379, db=0, password='123456')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
