# @version: python37
# @author: rgc
# time: 2018/11/13 20:22
#
# import logging
# from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
#
# logger = logging.getLogger('carrier')
# logger.setLevel(logging.INFO)
# log_path = 'carrier.log'
# # 按照文件超过一定大小时备份
# max_size = 1024 * 1024 * 20
# backupCount = 100
# delay = True
# fh = RotatingFileHandler(log_path, encoding='UTF-8', maxBytes=max_size, backupCount=backupCount, delay=delay)
# fh.setLevel(logging.DEBUG)
#
# # 按照时间备份
# # when 备份频率
# # interval 备份间隔（秒为单位）
# # backupCount 备份数量
# th = TimedRotatingFileHandler('carrier_time.log', when='M', interval=60, backupCount=10, encoding='UTF-8', delay=True,
#                               utc=True)
# th.setLevel(logging.INFO)
# logger.addHandler(th)
#
# # 添加输出到控制台的日志数据
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
#
# # 所有日志统一格式
# formatter = logging.Formatter(
#     '''{"asctime": %(asctime)s , "message": %(message)s ,"process": %(process)s ,"thread": %(thread)s }''')
# fh.setFormatter(formatter)
#
# logger.addHandler(fh)
# logger.addHandler(ch)


# use config file
import json
import logging
import logging.config

from kafka import KafkaProducer

conf_log = 'logging.conf'
import os

# https://stackoverflow.com/questions/46017513/keyerror-formatters-in-logging-module 日志导入问题
# https://stackoverflow.com/questions/28054864/use-fileconfig-to-configure-custom-handlers-in-python handler导入问题

file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, conf_log), disable_existing_loggers=False)
logger = logging.getLogger('rgc')
# logger.debug('==========start logging===========')

kafka = None


def build_kafka_producer():
    global kafka
    # 配置
    KAFKA_HOSTS = '106.14.172.140:9092'
    kafka = KafkaProducer(bootstrap_servers=KAFKA_HOSTS,
                          client_id="log-id",
                          key_serializer=str.encode,
                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def kafka_send_log(params: dict):
    print('send first state!')
    kafka.send('topic', key='async_log', value=params)


def kafka_send_email(params: dict):
    print(params,'***')
    kafka.send('topic', key='async_error_email', value=params)
