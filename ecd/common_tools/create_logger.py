# coding:utf-8
"""
author: Allen
summary: 记录日志
datetime: 2018/12/9
python version: 3.x
"""
import logging


class Logger(object):
    def __init__(self):
        pass

    @staticmethod
    def create_logger(path="file.log", log_level=logging.DEBUG, encoding='utf-8'):
        """
        创建日志函数
        :param path: 日志文件路径
        :param log_level: 日志等级:logging.DEBUG/logging.INFO/ logging.WARNING/logging.ERROR/logging.CRITICAL
        :param encoding: 文件编码
        :return: logger
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        handler = logging.FileHandler(path, mode='a', encoding=encoding)
        handler.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # formatter = logging.Formatter("%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s:%(message)s")
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(handler)
        logger.addHandler(ch)
        return logger


logger = Logger.create_logger()

if __name__ == '__main__':
    pass
