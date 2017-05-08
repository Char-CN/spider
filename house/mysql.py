# coding:utf-8
from DBUtils.PooledDB import PooledDB
import MySQLdb

MYSQL_DATABASE = {
    'test': {
        'DBNAME': 'dw_dataservice',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '172.16.52.137',
        'PORT': 3306,
        'MINCACHED': 3,
        'MAXCACHED': 5,
    },
    'server': {
        'DBNAME': 'dw_dataservice',
        'USER': 'report',
        'PASSWORD': '=g9rLM?30Z2!',
        'HOST': '10.127.133.176',
        'PORT': 3307,
        'MINCACHED': 3,
        'MAXCACHED': 5,
    }
}

class Mysql(object):
    
    __dbpools = {}  # 连接池
    
    def __init__(self, conn):
        self.__conn = conn
    
    def select(self, sql):
        cursor = self.__conn.cursor()
        count = cursor.execute(sql)
        if count == 0 :
            return None
        return cursor.fetchall()
    
    def select_count(self, sql):
        cursor = self.__conn.cursor()
        count = cursor.execute(sql)
        return count
    
    def select_and_count(self, sql):
        cursor = self.__conn.cursor()
        count = cursor.execute(sql)
        return count, cursor.fetchall()
    
    def update(self, sql):
        cursor = self.__conn.cursor()
        count = cursor.execute(sql)
        cursor.execute('commit')
        return count
    
    def delete(self, sql):
        cursor = self.__conn.cursor()
        count = cursor.execute(sql)
        cursor.execute('commit')
        return count
    
    def insert(self, sql):
        cursor = self.__conn.cursor()
        count = cursor.execute(sql)
        cursor.execute('commit')
        return count
    
    def get_conn(self):
        return self.__conn
    
    @staticmethod
    #===========================================================================
    # create_by_instance    根据实例名返回DBHandler对象
    #    @instance    实例名，settings.DATABASES的键
    #===========================================================================
    def db(instance):
        if instance not in Mysql.__dbpools:
            Mysql.__dbpools[instance] = PooledDB(creator=MySQLdb,
                                          mincached=MYSQL_DATABASE[instance]['MINCACHED'],
                                          maxcached=MYSQL_DATABASE[instance]['MAXCACHED'],
                                          
                                          host=MYSQL_DATABASE[instance]['HOST'],
                                          port=MYSQL_DATABASE[instance]['PORT'],
                                          user=MYSQL_DATABASE[instance]['USER'],
                                          passwd=MYSQL_DATABASE[instance]['PASSWORD'],
                                          
                                          db=MYSQL_DATABASE[instance]['DBNAME'],
                                          use_unicode=True,
                                          charset='utf8')
        return Mysql(Mysql.__dbpools[instance].connection())

