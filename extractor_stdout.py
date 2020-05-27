#! /usr/bin/python
# coding=utf-8

from settings import *
import os
import pandas as pd

def ReadFile(sftp, RemoteFile):
    """
    获取stdout标准输出流的方式读取单个文件
    sftp: paramiko.SFTPClien对象
    RemoteFile: 远程文件
    return: 文件读取操作执行完毕，返回data -> DataFrame
    """
    stdout = sftp.open(RemoteFile,"r")
    stdout_read = stdout.read()
    print(type(stdout_read))
    data = pd.read_excel(stdout_read, sheet_name="近180天叶子类目购买偏好_新")
    print(data)
    stdout.close() 
    # return data

def ReadFileTree(sftp, RemoteDir):
    """
    读取整个目录下的文件
    sftp: paramiko.SFTPClien对象
    RemoteFile: 远程文件
    return: 文件读取完毕，返回"complete"提示
    """
    for file in sftp.listdir(RemoteDir):
        Remote = os.path.join(RemoteDir, file)
        print(file.find("."))
        if file.find(".") == -1:
            ReadFileTree(sftp, Remote)
        else:
            ReadFile(sftp, Remote)
    return "complete"




if __name__ == '__main__':
    print(ReadFileTree(sftp, remote))