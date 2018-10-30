# coding:utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	REDIS_URL = "redis://:@localhost:6379/4"
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	TOKEN_EXPIRE = 3600 * 2
	DEBUG = True
	SECRET_KEY = 'Rgc is a wonderful boy!!'

	# 启用缓慢查询记录功能
	SQLALCHEMY_RECORD_QUERIES = True
	FLASKY_DB_QUERY_TIMEOUT = 0.1

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	# 此变量为数据库密码
	MYSQL_PASSWORD = ''
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_POOL_RECYCLE = 2400
	SQLALCHEMY_POOL_SIZE = 3
	SQLALCHEMY_MAX_OVERFLOW = 5
	SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{MYSQL_PASSWORD}@127.0.0.1:3306/userpermission'


class TestConfig(Config):
	REDIS_URL = "redis://:@localhost:6379/1"


class ProductionConfig(Config):
	DEBUG = False


config = {
	'dev': DevelopmentConfig,
	'test': TestConfig,
	'pro': ProductionConfig
}
