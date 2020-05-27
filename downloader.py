#! /usr/bin/python
# coding=utf-8

from settings import *
import os
 
class sftp_downloader(): 
    def __init__(self, sftp, LocalDir: str, RemoteDir: str):
        """
        下载sftp上的文件
        sftp: paramiko.SFTPClien对象
        LocalFile: 本地文件
        RemoteFile: 远程文件
        """
        self.sftp = sftp
        self.LocalDir = LocalDir
        self.RemoteDir = RemoteDir
        self._Local_cwd = None
        self._Remote_cwd = None

    def DownLoadFile(self):  
        """
        下载单个文件
        sftp: paramiko.SFTPClien对象
        LocalFile: 本地文件
        RemoteFile: 远程文件
        return: 下载操作执行完毕，返回True
        """
        if os.path.exists(self._Local_cwd):
            print("已存在文件：{}".format(self._Local_cwd))
            return False
        else:
            print(">>>准备下载：{}".format(self._Remote_cwd))
            file_handler = open(self._Local_cwd, 'wb')
            self.sftp.get(self._Remote_cwd, self._Local_cwd)          # 下载路径下文件
            file_handler.close()
            print(" >>已下载：{}！\n".format(self._Local_cwd))
            return True
    
    def DownLoadFileTree(self): 
        """
        下载整个目录下的文件
        sftp: paramiko.SFTPClien对象
        LocalDir: 本地文件路径
        RemoteDir: 远程文件路径
        return: 下载完成，返回"complete"提示
        """
        Local = self._Local_cwd if self._Local_cwd != None else self.LocalDir
        Remote = self._Remote_cwd if self._Remote_cwd != None else self.RemoteDir
        if not os.path.exists(Local):
            print(">>>本地路径不存在：{}".format(Local))
            print(" >>创建：{}".format(Local))
            os.makedirs(Local)
        for file in self.sftp.listdir(Remote):
            self._Local_cwd = os.path.join(Local, file)
            self._Remote_cwd = os.path.join(Remote, file)
            if file.find(".") == -1:                              # 判断是否是文件
                if not os.path.exists(self._Local_cwd):
                    print(">>>本地路径不存在：{}".format(self._Local_cwd))
                    print(" >>创建：{}".format(self._Local_cwd))
                    os.makedirs(self._Local_cwd)
                self.DownLoadFileTree()
            else:                                                 # 是文件就下载
                if self.DownLoadFile():
                    pass
                else:
                    print("<-- 不需要下载 --> \n")
        return "complete"
 
 

if __name__ == '__main__':
    sd = sftp_downloader(sftp,local,remote)
    print(sd.DownLoadFileTree())