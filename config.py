#'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
import os
SECRET_KEY = os.urandom(24)
#数据库的名称
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'website'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD,
HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False