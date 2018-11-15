from ups.log_middleware import logger, build_kafka_producer, kafka_send_log, kafka_send_email

__version__ = '0.1'
__author__ = 'RGC'
__date__ = '2018-10-25'

import copy

from flask import g, current_app, Blueprint
from flask_sqlalchemy import get_debug_queries

import ups.constant as cs
from ups import db, redis_store
from ups.constant import ROLE_TYPE as role
from ups.models import User, Acticle
from ups.service.decorator import request_info, v_login
from ups.service.public_service import request_data, try_check_request_data, gen_one_password, mobile_re, get_token
from ups.service.public_service import resq_wrapper as rw

public_blueprint = Blueprint('public', __name__)

SESSION = db.session


@public_blueprint.before_request
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


@public_blueprint.teardown_request
def handle_teardown_request(ex):
    SESSION.remove()


@public_blueprint.after_app_request
def after_request(response):
    # 录影响性能的缓慢数据库查询
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_DB_QUERY_TIMEOUT']:
            logger.warning('#####Slow query:%s \nParameters:%s \nDuration:%fs\nContext:%s\n #####' %
                           (query.statement, query.parameters, query.duration, query.context))
    return response


@public_blueprint.route('/account', methods=['POST'])
@request_info
def register():
    """
    所有用户注册接口
    参数：
    password str 必传
    mobile str 必传
    role_type int 必传
    """
    request_dict = try_check_request_data(request_data(), ['password', 1, 1], ['mobile', 1, 1],
                                          ['role_type', 0, 1])
    try:
        password = gen_one_password(request_dict['password'])
        mobile = request_dict['mobile']
        role_type = request_dict['role_type']
    except:
        return rw(cs.REQUEST_GET_VAL_fAIL, 3)
    user_info = {'password': password, 'mobile': mobile, 'role_type': role_type}
    if role_type not in [role['admin'], role['user']]:
        return rw(cs.REQUEST_GET_VAL_fAIL, 1)
    if not mobile_re(mobile):
        return rw(cs.REQUEST_GET_VAL_fAIL, 2)
    if User.exist([User.mobile == user_info['mobile']]):
        return rw(cs.REGISTERED)
    if User.create(user_info):
        return rw(cs.OK)
    return rw(cs.DB_COMMIT_ERR)


@public_blueprint.route('/test_log', methods=['GET'])
@request_info
def test_log():
    logger.error('one!')
    # build_kafka_producer()
    # kafka_send_log({'message': 'this is a message'})
    # kafka_send_email(
    #     {'email': '2020956572@qq.com', 'error_message': 'this is a error message!', 'service_name': 'rgc server'})
    return rw(cs.OK)


@public_blueprint.route('/account', methods=['GET'])
@request_info
def login():
    """
    所有用户登录接口
    参数：
    password str 必传
    mobile str 必传
    """
    request_dict = try_check_request_data(request_data(), ['password', 1, 1], ['mobile', 1, 1])
    try:
        password = gen_one_password(request_dict['password'])
        mobile = request_dict['mobile']
    except:
        return rw(cs.REQUEST_GET_VAL_fAIL)
    user_dict = User.info([User.mobile == mobile], 'info')
    if not user_dict:
        return rw(cs.NO_USER)
    if user_dict['password'] != password:
        return rw(cs.PASSWD_ERR)

    token = get_token(mobile)

    user_json = copy.deepcopy(user_dict)
    user_json.update({'token': token})
    user_json.pop('password')
    redis_store.hmset('token:%s' % token, user_json)
    redis_store.expire('token:%s' % token, current_app.config['TOKEN_EXPIRE'])
    return rw(cs.OK, user_json)


@public_blueprint.route('/acticle', methods=['GET'])
@request_info
@v_login
def get_acticle():
    """
    所有用户获取未删除文章（自己的文章或作全部用户的文章）
    参数：
    only_self int 必传(1:只看自己的文章 2：全部)
    page_size int 必传
    page_index int 必传
    """
    user = g.user

    request_dict = try_check_request_data(request_data(), ['only_self', 0, 1],
                                          ['page_size', 0, 1], ['page_index', 0, 1])
    try:
        only_self = request_dict['only_self']
        page_size = request_dict['page_size']
        page_index = request_dict['page_index']
    except:
        return rw(cs.REQUEST_GET_VAL_fAIL)
    if only_self == 1:  # 只查看自己的文章
        result = Acticle.pagination([Acticle.uid == user.id, Acticle.status == Acticle.acticle_status['undel']],
                                    page_index,
                                    page_size, 'info')

    else:  # 查看所有文章
        result = Acticle.pagination([Acticle.status == Acticle.acticle_status['undel']], page_index,
                                    page_size, 'info')
    return rw(cs.OK, result)


@public_blueprint.route('/acticle', methods=['DELETE'])
@request_info
@v_login
def delete_acticle():
    """
    所有用户删除文章（管理员可以删除所有用户的未被删除的文章，普通用户只能删除自己的未被删除的文章）
    参数：
    acticle_id int 必传
    """
    user = g.user
    request_dict = try_check_request_data(request_data(), ['acticle_id', 0, 1])
    try:
        acticle_id = request_dict['acticle_id']
    except:
        return rw(cs.REQUEST_GET_VAL_fAIL)
    # 判断此文章是否存在
    if not Acticle.exist([Acticle.id == acticle_id, Acticle.status == Acticle.acticle_status['undel']]):
        return rw(cs.NO_EXIST_ACTICLE_PER)
    # 如果是普通用户则判断自己的文章是否存在
    if user.role_type == User.user_role['user']:
        if not Acticle.exist(
                [Acticle.uid == user.id, Acticle.id == acticle_id, Acticle.status == Acticle.acticle_status['undel']]):
            return rw(cs.NO_ME_ACTICLE_PER)
    # 删除文章
    if Acticle.update([Acticle.id == acticle_id], {'status': Acticle.acticle_status['del']}):
        return rw(cs.OK)
    return rw(cs.DB_COMMIT_ERR)
