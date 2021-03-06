import traceback

import ups.constant as cs
from ups.info import logger
from ups.service.public_service import resq_wrapper as rw
from ups.user.views import user_blueprint


@user_blueprint.errorhandler(Exception)
def unhandled_exception(e):
	logger.error('Unhandled Exception: %s', e)
	logger.error(traceback.format_exc())
	return rw(cs.SERVER_ERR), 500
