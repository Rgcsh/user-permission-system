__version__ = '0.1'
__author__ = 'RGC'
__date__ = '2018-10-25'

from flask import g, current_app, Blueprint

import ups.constant as cs
from ups import db, redis_store
from ups.models import User, Acticle
from ups.service.decorator import request_info, v_login, v_admin_role
from ups.service.public_service import request_data, try_check_request_data
from ups.service.public_service import resq_wrapper as rw

admin_blueprint = Blueprint('admin', __name__)

SESSION = db.session


@admin_blueprint.before_request
def before_request():
	token = request_data().get('token')
	if token:
		get_token = redis_store.hgetall('token:%s' % token)
		if get_token:
			mobile = get_token[b'mobile']
			user_obj = User.get_obj_by_field([User.mobile == mobile])
			if not user_obj:
				return rw(cs.NO_USER)
			g.user = user_obj
			redis_store.expire('token:%s' % token, current_app.config['TOKEN_EXPIRE'])
		else:
			return rw(cs.TOKEN_EXPIRE)
	return


@admin_blueprint.teardown_request
def handle_teardown_request(ex):
	SESSION.remove()


@admin_blueprint.route('/acticle', methods=['POST'])
@request_info
@v_login
@v_admin_role
def add_acticle():
	'''
	管理员新增文章
	参数：
	content str 必传 文章内容
	'''
	user = g.user
	request_dict = try_check_request_data(request_data(), ['content', 1, 1])
	request_dict.update({'uid': user.id, 'role_type': user.role_type})
	if Acticle.create(request_dict):
		return rw(cs.OK)
	return rw(cs.DB_COMMIT_ERR)


@admin_blueprint.route('/acticle', methods=['PUT'])
@request_info
@v_login
@v_admin_role
def update_acticle():
	'''
	管理员更新文章
	参数：
	content str 必传 文章内容
	acticle_id int 必传 文章id
	'''
	user = g.user
	request_dict = try_check_request_data(request_data(), ['content', 1, 1], ['acticle_id', 0, 1])
	try:
		content = request_dict['content']
		acticle_id = request_dict['acticle_id']
	except:
		return rw(cs.REQUEST_GET_VAL_fAIL)
	if not Acticle.exist(
			[Acticle.uid == user.id, Acticle.id == acticle_id, Acticle.status == Acticle.acticle_status['undel']]):
		return rw(cs.NO_ACTICLE_PER)
	if Acticle.update([Acticle.uid == user.id, Acticle.id == acticle_id], {'content': content}):
		return rw(cs.OK)
	return rw(cs.DB_COMMIT_ERR)
