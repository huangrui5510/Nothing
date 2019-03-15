# coding:utf-8
"""
author: Allen
email: lingyunzou@aliyun.com
datetime:
python version: 3.x
summary: sqlite database handler
install package:
"""
import logging
from functools import wraps
from sqlite3 import connect

logger = logging.getLogger(__name__)


def roll_back(func):
    """类中使用的装饰器，在写数据库操作的时候使用"""

    @wraps(func)
    def _inner(self, *args, **kwargs):
        """遇到异常的时候回滚操作"""
        self.connection_db()
        try:
            func(self, *args, **kwargs)
            self.commit()
            return True, 'no error'
        except Exception as e:
            logger.error(str(e))
            self.connection.rollback()
            return False, 'occur error'

    return _inner


class SqliteHandler(object):
    def __init__(self, db_con):
        self.db_con = db_con
        self.connection = None
        self.cursor = None

    def connection_db(self):
        """获取数据库连接和游标对象"""
        if self.connection is None:
            conn = connect(self.db_con)
            self.connection = conn
            self.cursor = conn.cursor()
            return conn
        return None

    def commit(self):
        """提交修改"""
        if self.connection is not None:
            self.cursor.close()
            self.connection.commit()

    @roll_back
    def excute(self, sql, args=None):
        """执行sql，该执行需要对数据库有修改"""
        self.cursor.execute(sql, args)

    def fetchone(self, sql):
        """查询数据，获取第一条查询结果"""
        self.connection_db()
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res

    def fetchall(self, sql):
        """查询数据，获取所有查询结果"""
        self.connection_db()
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    @roll_back
    def insert(self, sql, seq):
        """插入数据"""
        self.cursor.executemany(sql, seq)

    def __del__(self):
        """关闭连接"""
        try:
            if self.cursor is not None:
                self.cursor.close()
        except Exception:
            pass

        try:
            if self.connection is not None:
                self.connection.close()
        except Exception:
            pass

    def __enter__(self):
        self.connection_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()
