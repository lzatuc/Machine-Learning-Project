from douban.douban.settings import MYSQL_DBNAME
from douban.douban.settings import MYSQL_USER
from douban.douban.settings import MYSQL_PASSWORD
from douban.douban.settings import MYSQL_HOST
import pymysql


class MySqlPersistenceHelper:
    @staticmethod
    def get_connection(host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DBNAME,
                       charset='utf8'):
        connection = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        return connection

    @staticmethod
    def execute_sql(connection, cursor, sql):
        try:
            cursor.execute(sql)
            connection.commit()
        except:
            connection.rollback()
