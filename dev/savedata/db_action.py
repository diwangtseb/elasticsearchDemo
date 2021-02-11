# -*- coding:utf-8 -*-
import sqlite3
import threading


# 单例模式
class SqliteDatabase(object):
    _instance_lock = threading.Lock()

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with SqliteDatabase._instance_lock:
                if not hasattr(cls, '_instance'):
                    SqliteDatabase._instance = super().__new__(cls)
        return SqliteDatabase._instance

    def __init__(self, dbsource: str):
        """
        :type dbsource: str
        """
        print(f"database connect successfully!")
        self.conn = sqlite3.connect(dbsource, check_same_thread=False)
        self.c = self.conn.cursor()

    def exec_sql(self, sql: str):
        """:param sql is sqlite3 sql insert"""
        self.c.execute(sql)
        self.conn.commit()

    def select_sql(self, sql: str):
        """:param sql sqlite3 sql select"""
        self.conn.row_factory = self.dict_factory
        self.c = self.conn.cursor()
        sql_res = self.c.execute(sql).fetchall()
        return sql_res

    @staticmethod
    def dict_factory(cursor, row):
        """将sql查询结果整理成字典形式"""
        d = {}
        for index, col in enumerate(cursor.description):
            d[col[0]] = row[index]
        return d

    def __del__(self):
        self.conn.close()
