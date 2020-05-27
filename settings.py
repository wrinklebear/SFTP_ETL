#! /usr/bin/python
# coding=utf-8

import paramiko
from paramiko.client import AutoAddPolicy
# from ftplib import FTP

"""SFTP连接参数"""
host = '52.82.3.13'                              # SFTP主机
port = 22                                        # 端口
username = 'yhdata'                              # 用户名
password = 'yhdata'                              # 密码


"""SFTPClient对象，用户操作文件读写"""
sf = paramiko.Transport((host, port))
sf.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(sf)
local = '/PZ/SFTP_ETL/downloads'                 # 本地文件路径
remote = '/yhdata'                               # 远程文件或目录

"""client对象，获取stdout标准输出流，用以操作文件读写"""
client = paramiko.SSHClient() 
client.load_system_host_keys() 
client.set_missing_host_key_policy(AutoAddPolicy()) 
client.connect(hostname=host, username=username, password=password) 
stdin, stdout, stderr = client.exec_command(host) 

# session = FTP(host, username, password)        
# sftp需要加密，没法用ftp的模块，#
# 报错ftplib.error_perm: 530 Non-anonymous sessions must use encryption.


# 数据库连接字符串，create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
# 使用windows凭证：engine = sqlalchemy.create_engine('mssql+pymssql://*server_name*\\SQLEXPRESS/*database_name*?trusted_connection=yes')
  
DIALECT='mysql'
DRIVER='pymysql'
DIALECT1='mssql'
DRIVER1='pymssql'
USERNAME='root'
USERNAME1='sa'
PASSWORD='648451kobe'
SERVER_NAME='.'
HOST='localhost'
PORT='3306'
PORT1='1433'
DATABASE='test'
DATABASE1='Shopper_Profile'
# mssql
DB_CONNECT_STRING_LOCAL='{}+{}://{}:{}@{}:{}/{}?charset:utf8'.format(DIALECT1,DRIVER1,USERNAME1,PASSWORD,HOST,PORT1,DATABASE1)
# mysql
DB_CONNECT_STRING='{}+{}://{}:{}@{}:{}/{}?charset:utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)