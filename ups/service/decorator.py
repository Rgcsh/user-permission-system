from functools import partial
from functools import wraps
from time import time

from flask import g
from flask import request

from ups import constant as cs
from ups import redis_store
from ups.info import logger
from ups.service.public_service import request_data, resq_wrapper as rw


# 请求参数
def request_info(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		request_infos = ' '.join(
			[request.method, request.path])
		logger.info('Request: %s', request_infos)
		func_return = f(*args, **kwargs)
		response_info = str(func_return.response[0])
		if request.method == 'POST':
			logger.info('Response:%s', response_info)
		else:
			logger.info('Response:%s', response_info)
		func_return.headers.__dict__.get('_list').append(("Access-Control-Allow-Origin", "*"))
		return func_return

	return decorator


# 判断能否登录
def v_login(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		token = request_data().get('token')
		if not token:
			return rw(cs.NO_TOKEN)
		mobile = redis_store.hmget('token:%s' % token, 'mobile')
		if not mobile:
			return rw(cs.TOKEN_EXPIRE)
		return f(*args, **kwargs)

	return decorator


# 计算接口所花费时间
def timing(func=None):
	if func is None:
		return partial(timing)

	@wraps(func)
	def _wrapper(*args, **kwargs):
		start_time = time()
		result = func(*args, **kwargs)
		end_time = time()
		print('运行花费时间：{:.6f}s。'.format(end_time - start_time))
		return result

	return _wrapper


# 普通用户权限
def v_user_role(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		user = g.user
		role = user.role_type
		logger.info('client: %s, path: %s, method: %s' % (request.remote_addr, request.path, request.method))
		if role != cs.ROLE_TYPE['user']:
			return rw(cs.NOT_ALLOW)
		return f(*args, **kwargs)

	return decorator


# 管理员权限
def v_admin_role(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		user = g.user
		role = user.role_type
		logger.info('client: %s, path: %s, method: %s' % (request.remote_addr, request.path, request.method))
		if role != cs.ROLE_TYPE['admin']:
			return rw(cs.NOT_ALLOW)
		return f(*args, **kwargs)

	return decorator
