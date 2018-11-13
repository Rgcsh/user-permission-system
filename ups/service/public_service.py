import cgi
import datetime
import hashlib
import json
import re
import time

from flask import request, jsonify

from ups import constant as cs
from ups.info import logger


def request_data():
	if request.method in ('POST', 'PUT'):
		if hasattr(request, 'json') and request.json:
			return request.json
		else:
			return request.values
	else:
		return request.values


def resq_wrapper(code, rval=None):
	return jsonify({'code': code, 'errmsg': cs.ERR_MSG[code], 'data': rval})


# 记录日志
# 参数  remote_addr:请求IP地址，path:接口名字，method:请求方法，action:操作内容，result_code:操作结果编号，user_id:操作人用户id
def log_write(remote_addr, path, method, action, result_code, user_id):
	logger.info('client: %s, path: %s, method: %s, action:%s, result:%s, time:%s, user_id:%s' % (
		remote_addr, path, method, action, result_code, datetime.datetime.now(), user_id))


def str_to_list(str):
	return json.loads(str)


# 判断数据是否为空
def is_none(data):
	if data is None or data == 'null':
		return ''
	return data


# 获取用户信息
# 参数  user:用户对象
def get_user_message(user):
	return {'user_role': user.role, 'user_id': user.id}


# 判断用户传参问题
# 尽量所有参数全传,str类型非必传,int类型必传
def try_check_request_data(request_data, *lists):
	# item[1] 0 int; 1 str; 2 nothing;3 float
	# item[2] 0:非必传; 1必传
	try:
		dic = dict()
		for item in lists:
			if item[2] == 1:
				if request_data.get(item[0]) == 'null' or request_data.get(item[0]) is None or request_data.get(
						item[0]) == '':
					return resq_wrapper(cs.REQUEST_GET_VAL_fAIL, request_data + '缺少必传值！==^~~^==')
			value = request_data.get(item[0], '')
			key = item[0]
			type = item[1]
			if type == 0:
				if value == '':
					dic.update({key: None})
				else:
					dic.update({key: int(value)})
			elif type == 1:
				# 不信任用户输入，转义html标签
				dic.update({key: cgi.escape(str(value))})
			elif type == 2:
				dic.update({key: value})
			elif type == 3:
				if value == '':
					dic.update({key: None})
				else:
					dic.update({key: float(value)})
		return dic
	except TypeError as e:
		logger.error(e)
		return resq_wrapper(cs.REQUEST_GET_VAL_fAIL, request_data)
	except ValueError as  e:
		logger.error(e)
		return resq_wrapper(cs.REQUEST_GET_VAL_fAIL, request_data)
	except Exception as e:
		logger.warning(e)
		return jsonify({'code': cs.EXCEPTION, 'errmsg': 'unexpected error : s%' % e, 'data': request_data})


def str_encode(field):
	return field.encode('utf8')


# one次md5加密
def gen_one_password(password):
	_passwd = str_encode(password)
	m2 = hashlib.md5()
	m2.update(_passwd)
	m3 = m2.hexdigest()
	return m3


def get_token(mobile):
	_mobile = str_encode(mobile)
	_time = str_encode(str(int(time.time())))
	m = hashlib.md5()
	m.update(_mobile)
	m.update(_time)
	return m.hexdigest()


Mobile_Regexp = re.compile(r'^1[3456789][0-9]{9}$')
List_to_str_Regexp = re.compile(r'(\'|\[|\])')


def list_to_str(list):
	return re.sub(List_to_str_Regexp, '', str(list))


def mobile_re(mobile):
	return Mobile_Regexp.match(mobile)


def get_this_time():
	return datetime.datetime.now()
