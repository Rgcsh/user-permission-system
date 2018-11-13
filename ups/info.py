import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

logger = logging.getLogger('carrier')
logger.setLevel(logging.INFO)

# 按照文件超过一定大小时备份
fh = RotatingFileHandler('carrier.log', encoding='UTF-8', maxBytes=1024 * 1024 * 20, backupCount=10, delay=True)
fh.setLevel(logging.DEBUG)

# 按照时间备份
# when 备份频率
# interval 备份间隔（秒为单位）
# backupCount 备份数量
th = TimedRotatingFileHandler('carrier_time.log', when='M', interval=60, backupCount=10, encoding='UTF-8', delay=True,
                              utc=True)
th.setLevel(logging.INFO)

# 添加输出到控制台的日志数据
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# 所有日志统一格式
formatter = logging.Formatter('''%(asctime)s - %(message)s''')
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(th)
