#! /usr/bin/python
# coding=utf-8

from settings import *
import os
import pandas as pd
from db import *
import datetime
import time

class sftp_extactor():
    def __init__(self, sftp, RemoteDir: str, switcher:'int > 0' =0):
        """
        读取sftp上的excel/csv文件
        sftp: paramiko.SFTPClien对象
        RemoteFile: 远程文件
        switcher: 0 -> excel; 1 -> csv; 0 for default which is recommaneded
        """
        if not isinstance(switcher, int):
            raise TypeError("'switcher' should be Int.")
        self.sftp = sftp
        self.RemoteDir = RemoteDir
        self._cwd = None
        self.switcher = switcher
        self.file = None
        self.mtime = None
        self.fileName = None
        self.fileNames = None
        self.threhold = None

    def timeTransfor(self):
        """
        dir(stat),查看SFTPAttributes对象的属性和方法
        # stat.st_atime（数据的最后访问时间）
        # stat.st_mtime（数据的最后修改时间）
        """
        cwd = '/'.join(self._cwd.split('\\'))
        stat = self.sftp.stat(cwd)
        time_local1 = time.localtime(stat.st_atime)
        time_local2 = time.localtime(stat.st_mtime)
        atime = time.strftime("%Y-%m-%d %H:%M:%S",time_local1)
        mtime = time.strftime("%Y-%m-%d %H:%M:%S",time_local2)
        return atime, mtime


    def timeThrehold(self):
        """
        对准备下载的文件的上传时间作微增处理
        """
        st=time.strptime(self.mtime, "%Y-%m-%d %H:%M:%S")
        if st[4]>=0 and st[4]<=58:
            st[4] = st[4]+1 
        else:
            st[3] = st[3]+1
        self.threhold = datetime.datetime(
            st[0],st[1],st[2],st[3],st[4],st[5]
        ).strftime("%Y-%m-%d %H:%M:%S")

    
    def queryMax(self):
        """
        从表ShopperProfile中取上传时间最大值
        """
        upload_times = engine.execute(
            "SELECT uploadTime FROM ShopperProfile"
        ).fetchall()
        if upload_times:
            self.max_time = max(upload_times)[0]
            return True
        else:
            return False


    def queryFileName(self):
        """
        从表ShopperProfile中取所有fileName
        """
        fileNames = engine.execute(
            """SELECT fileName 
               FROM ShopperProfile
               Group By fileName """
        ).fetchall()
        if fileNames:
            self.fileNames = [f[0] for f in fileNames]
            return True
        else:
            return False 



    def ReadFile(self):
        """
        读取单个文件
        sftp: paramiko.SFTPClien对象
        RemoteFile: 远程文件
        return: 文件读取操作执行完毕，返回data -> DataFrame
        """
        self.fileName = self.file.split('.')[0]                 # if fileName.lower() in set(tables.keys()): 如果以fileName作为表名，用这句排重
        print(self.fileName)
        fList=[]
        self.max_time = self.max_time if self.queryMax() else "1900-01-01 00:00:00"
        self.fileNames = set(self.fileNames) if self.queryFileName() else set(fList)
        print("*"*30)
        print("已存储的最大文件上传时间：{}".format(self.max_time))
        # self.timeThrehold()
        print("准备下载的文件{}的上传时间：{}".format(self.fileName, self.mtime))
        print("*"*30)

        if self.max_time <= self.mtime and self.fileName not in self.fileNames:   
            # 如果库内最大上传时间小于即将下载文件的上传时间，且大类未上传过
            print(">>>准备读取：{}".format(self._cwd))
            print(self._cwd)
            trans_cwd = '/'.join(self._cwd.split('\\'))
            print(trans_cwd)
            with self.sftp.open(trans_cwd, "rb") as f:      # 读取路径下文件              
                if self.switcher == 0: 
                    # 读取excel文件
                    data = pd.read_excel(f, None)
                    chunks=[]
                    now = datetime.datetime.now()
                    for i, k in enumerate(list(data.keys())):
                        exec("df{} = pd.read_excel(f, sheet_name='{}')".format(i, k))
                        exec("df{}.columns=['crowdName','itemName','TGI','Percentage']".format(i))
                        exec("df{}['Dim'] = '{}'".format(i, k))
                        exec("df{}['fileName'] = '{}'".format(i, self.fileName))
                        exec("df{}['uploadTime'] = '{}'".format(i, self.mtime))
                        exec("df{}['createTime'] = '{}'".format(i, now))
                        chunks.append(eval("df{}".format(i)))
                    df = pd.concat(chunks, ignore_index=False)
                    df.to_sql("ShopperProfile", con=engine, if_exists='append', index_label='index')
                    
                    # 也可通过pd.ExcelFile对象的sheet_names获取表单名
                    # df = pd.ExcelFile(f)
                    # print(df.sheet_names)
                    
                    print(" >>读取完毕！：{} \n".format(self._cwd))
                    # return df
                elif self.switcher == 1:   
                    # 读取CSV格式用这句decode             
                    data = f.read().decode("gbk")
                    print(data)
                    print(" >>读取完毕！：{} \n".format(self._cwd))
                    # return data
                else:
                    raise TypeError("'switcher' should be 0 or 1.")
            return True
        else:                                             # 如果库内最大上传时间大于将下载文件的上传时间，不更新
            print("数据'{}'已更新过".format(self.fileName))  
            return False
            

    def ReadFileTree(self):
        """
        读取整个目录下的文件
        sftp: paramiko.SFTPClien对象
        RemoteFile: 远程文件
        return: 文件读取完毕，返回"complete"提示
        """
        Remote = self._cwd if self._cwd != None else self.RemoteDir
        for file in self.sftp.listdir(Remote):
            self._cwd = os.path.join(Remote, file)
            self.file = file
            if file.find(".") == -1:
                self.ReadFileTree()
            else:
                self.mtime = self.timeTransfor()[1]
                if self.ReadFile():
                    pass
                else:
                    print("<-- 不需要读取更新 --> \n")
        return "complete"




if __name__ == '__main__':
    se = sftp_extactor(sftp, remote)
    # se.maxMtime()
    print(se.ReadFileTree())