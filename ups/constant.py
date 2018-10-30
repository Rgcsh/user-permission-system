OK = 1000
NO_EXIST_ACTICLE_PER = 1001
NO_ME_ACTICLE_PER = 1002
NO_ACTICLE_PER = 1003
SERVER_ERR = 1004
NOT_ALLOW = 1005
REGISTERED = 1006
NO_USER = 1007
NO_TOKEN = 1008
PASSWD_ERR = 1009
TOKEN_EXPIRE = 1010
DB_COMMIT_ERR = 1011
REQUEST_GET_VAL_fAIL = 1012
ERR_MSG = {
	1000: 'success',
	1001: '此文章不存在或已删除！',
	1002: '没有操作此文章的权限或此文章已删除！',
	1003: '没有操作此文章的权限！',
	1004: 'server err!',
	1005: '没有权限!',
	1006: '手机号已经注册过！',
	1007: '用户不存在！',
	1008: 'NO TOKEN',
	1009: '密码错误!',
	1010: 'token过期!',
	1011: 'db commit transaction error!',
	1012: '数据类型取值失败!',
}

ROLE_TYPE = {
	"admin": 1,  # admin
	"user": 2,  # normal user
}
