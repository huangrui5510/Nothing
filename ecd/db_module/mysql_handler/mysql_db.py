# coding:utf-8
"""
author: Allen
summary: 操作mysql数据库
datetime: 2018/12/9
python version: 3.x
install package:
    pip install mysqlclient>=1.3.14
"""
import MySQLdb
import logging

logging.basicConfig(level=logging.DEBUG)


class MysqlDB(object):
    def __init__(self, db_info, logger=logging):
        self.db_info = db_info
        self.logger = logger
        self.conn = self.connection()

    def insert(self, sql, *args):
        """
        插入数据
        :param sql:
        :param args:
        :return: None
        """
        self.excute(sql, *args)

    def bulk_insert(self, sql, data_seq, bulk_num=5000):
        """
        批量插入数据
        :param sql: 插入sql
            insert into tab_name(field_1, field_2) values(%s, %s)
        :param data_seq: 插入数据列表
            [(v1_1, v1_2), (v2_1, v2_2),...]
        :param bulk_num: 单次插入条目数
        :return: None
        """
        num = len(data_seq)
        for e_i in range(0, num, bulk_num):
            e_bulk = data_seq[e_i:e_i + bulk_num]
            state = self.excute_many(sql, e_bulk)
            if not state:
                for row in e_bulk:
                    self.insert(sql, row)

    def excute(self, sql, *args):
        """
        带参数执行sql
        :param sql:
        :param args:
        :return: None
        """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, args)
            self.conn.commit()
            cur.close()
        except MySQLdb.Error as e:
            self.logger.error(str(e))
            self.conn.rollback()
            raise MySQLdb.Error(str(e))


    def excute_many(self, sql, *args):
        """

        :param sql:
        :param args:
        :return: True/False
        """
        cur = self.conn.cursor()
        try:
            cur.executemany(sql, args)
            cur.close()
            return True
        except Exception as e:
            self.logger.error(str(e))
            self.conn.rollback()
            cur.close()
            return False


    def fetch_one(self, sql, *args):
        """
        查询一条数据
        :param sql:
        :param args:
        :return: list/None
        """
        cur = self.conn.cursor()
        try:
            cur.execute(sql, args)
            res = cur.fetchone()
            cur.close()
            return res
        except Exception as e:
            self.logger.error(str(e))
            cur.close()
            return None

    def fetch_all(self, sql, *args):
        """
        查询所有数据
        :param sql:
        :param args:
        :return: list/None
        """
        cur = self.conn.cursor()
        try:
            cur.execute(sql, args)
            res = cur.fetchall()
            cur.close()
            return res
        except Exception as e:
            self.logger.error(str(e))
            cur.close()
            return None

    def connection(self):
        """
        连接数据库
        :return: 数据库连接对象/None
        """
        try:
            con = MySQLdb.connect(host=self.db_info.host, port=self.db_info.port, password=self.db_info.password,
                                  user=self.db_info.user, db=self.db_info.db, charset=self.db_info.charset)
            return con
        except MySQLdb.Error as e:
            self.logger.error(str(e))
            return None