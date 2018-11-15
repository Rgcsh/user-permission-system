from sqlalchemy import and_, update, delete, select, func, or_
from sqlalchemy.exc import SQLAlchemyError

from ups.log_middleware import logger
from ups.service.public_service import list_to_str

__version__ = '0.1'
__author__ = 'RGC'
__date__ = '2018-10-25'

import datetime

from ups import db


class _ModelPub(object):
	__tablename__ = None
	__keys_map__ = {
		'paging': [
		],
		'info': [
		]
	}

	@classmethod
	def get_obj_by_field(cls, search):
		return cls.query.filter(and_(*search)).first()

	@classmethod
	def create(cls, info: dict):
		order = cls(**info)
		db.session.add(order)
		try:
			db.session.commit()
		except SQLAlchemyError as e:
			logger.error('DB ERROR:%s', e)
			return False
		return True

	def to_dict(self, keys):
		d = {}
		for k in keys:
			d[k] = getattr(self, k)
		return d

	@classmethod
	def info(cls, search, field):
		# search list
		# field str
		ins = cls.query.filter(and_(*search)).first()
		if ins is None:
			return dict()
		return ins.to_dict(keys=cls.__keys_map__[field])

	@classmethod
	def info_all(cls, search, field):
		# 查询全部字段，再取部分值
		ins = cls.query.filter(and_(*search)).all()
		if ins is None:
			return
		return list(
			map(
				lambda x: x.to_dict(cls.__keys_map__[field]), ins
			)
		)

	@classmethod
	def info_some_sql(cls, search, field, other=''):
		# 查询部分字段
		field = list_to_str(cls.__keys_map__[field])
		sql = 'SELECT {field} FROM {tb_name} WHERE {search} {other}'.format(
			field=field,
			tb_name=cls.__tablename__,
			search=search,
			other=other
		)
		return map(
			dict, db.session.execute(sql).fetchall()
		)

	@classmethod
	def info_all_and_query(cls, search, *field):
		# search 传 list ,field 传 变量
		return db.session.query(*field).filter(and_(*search)).all()

	@classmethod
	def info_all_or_query(cls, search, *field):
		# search 传 list ,field 传 变量
		return db.session.query(*field).filter(or_(*search)).all()

	@classmethod
	def info_first_and_query(cls, search, *field):
		# search 传 list ,field 传 变量
		return db.session.query(*field).filter(and_(*search)).first()

	@classmethod
	def info_first_or_query(cls, search, *field):
		# search 传 list ,field 传 变量
		return db.session.query(*field).filter(or_(*search)).first()

	@classmethod
	def update(cls, search, data):
		# search list
		# data dict
		db.session.execute(
			update(cls).where(and_(*search)).values(**data)
		)
		try:
			db.session.commit()
		except SQLAlchemyError:
			db.session.rollback()
			return False

		return True

	@classmethod
	def delete(cls, search):
		# search list
		db.session.execute(delete(cls).where(and_(*search)))
		try:
			db.session.commit()
		except SQLAlchemyError:
			db.session.rollback()
			return False

		return True

	@classmethod
	def exist(cls, search):
		# search list
		return db.session.execute(
			select([func.count(cls.id)]).where(
				and_(*search)
			)
		).fetchone()[0] == 1

	@classmethod
	def map_dict(cls, sql):
		return map(dict, db.session.execute(sql))

	@classmethod
	def list_map_dict(cls, sql):
		return list(cls.map_dict(sql))

	@classmethod
	def get_sum(cls, sum_field, filter):
		c = db.session.execute(
			select([func.sum(sum_field)]).where(and_(*filter))
		).fetchone()[0] or 0
		return c

	@classmethod
	def get_count(cls, sum_field, filter):
		c = db.session.execute(
			select([func.count(sum_field)]).where(and_(*filter))
		).fetchone()[0] or 0
		return c

	@classmethod
	def pagination(cls, search, page_index, page_size, field):
		result = cls.query.filter(and_(*search)).paginate(int(page_index), int(page_size), False)
		result_list = []
		for item in result.items:
			result_list.append(item.to_dict(keys=cls.__keys_map__[field]))
		return result_list


# 用户表
class User(_ModelPub, db.Model):
	__tablename__ = 'user'
	user_role = {'admin': 1, 'user': 2}
	__keys_map__ = {
		'paging': [
		],
		'info': [
			'id', 'password', 'mobile', 'role_type', 'create_time'
		]
	}

	id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	password = db.Column('password', db.String(256), nullable=False, comment='密码')
	mobile = db.Column('mobile', db.String(64), unique=True, comment='手机号')
	role_type = db.Column('role_type', db.Integer, nullable=False, comment='用户权限1:admin 2:user')
	create_time = db.Column('create_time', db.TIMESTAMP, default=datetime.datetime.now(), comment='创建时间')


# 文章表
class Acticle(_ModelPub, db.Model):
	__tablename__ = 'acticle'
	acticle_status = {'undel': 1, 'del': 2}
	__keys_map__ = {
		'paging': [
			'id', 'uid', 'role_type', 'content', 'create_time', 'update_time'
		],
		'info': [
			'id', 'uid', 'role_type', 'content', 'create_time', 'update_time'
		]
	}

	id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	uid = db.Column('uid', db.Integer, nullable=False, index=True, comment='外键,指向user.id')
	role_type = db.Column('role_type', db.Integer, nullable=False, comment='用户权限,冗余字段')  # 1:admin 2:normal user
	content = db.Column('content', db.String(256), nullable=False, comment='文章内容')
	status = db.Column('status', db.SmallInteger, default=acticle_status['undel'], index=True,
					   comment='文章状态')  # 1：未删除 2：删除
	create_time = db.Column('create_time', db.TIMESTAMP, default=datetime.datetime.now(), comment='创建时间')
	update_time = db.Column('update_time', db.TIMESTAMP, comment='更新时间')
