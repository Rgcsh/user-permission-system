from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from ups.config import config

db = SQLAlchemy()
redis_store = FlaskRedis()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)
	redis_store.init_app(app)

	from ups.user.views import user_blueprint
	from ups.admin.views import admin_blueprint
	from ups.public.views import public_blueprint
	app.register_blueprint(user_blueprint, url_prefix='/user')
	app.register_blueprint(admin_blueprint, url_prefix='/admin')
	app.register_blueprint(public_blueprint, url_prefix='/public')

	return app
