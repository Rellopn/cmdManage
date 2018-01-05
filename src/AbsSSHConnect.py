# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import paramiko

from src.RemoteException import RemoteException


class AbsSSHConnect():
    _metaclass__ = ABCMeta
    """
        这是一个抽象类，链接到服务器后，需要上传文件等等操作，根据不同的命令需要重写其中到抽象方法。实现在
        执行命令前的一些操作，比如上传文件等等。
        当然也可以不写
        
        如果需要扩展程序的话，可以在继承此类的基础上扩展。
        :param settingInfo     格式 ：[
                                            {setting:xxxxYaml}
                                            {port:[7001,7002]}
                                            {slave:1}
                                            {username: root}
                                            {password: asd6614250}
                                            {ip: 192.168.1.157}
                                            {sshPort: 22}
                                            {workDir:'/root'}
                                            {cmd:[
                                                  {ls:'0'}
                                                  {pwd:'/root'}
                                                   ]}
                                             ]
    """

    def __init__(self, settingInfo, setting):
        self.settingInfo = settingInfo
        self.setting = setting

    def getConnect(self):
        """ 获得ssh端"""
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ip = self.settingInfo['ip']
        sshPort = int(self.settingInfo['sshPort'])
        name = self.settingInfo['username']
        pwd = str(self.settingInfo['password'])
        s.connect(ip, sshPort, name, pwd)
        return s

    def sshUpload(self, putFile, fileName):
        """ 上传文件 :param putFile 要上传端文件；:param fileName 上传到服务器到位置"""
        t = paramiko.Transport((self.settingInfo['ip'], int(self.settingInfo['sshPort'])))

        t.connect(username=self.settingInfo['username'],
                  password=str(
                      self.settingInfo['password']))  # 连接方式也可以用key，这里只需要将password=password改为pkey=key，其余的key代码与前面的一样

        sftp = paramiko.SFTPClient.from_transport(t)  # 使用t的设置方式连接远程主机
        # sftp.get('/home/pi/b.txt', 'b.txt')  # 下载文件
        sftp.put(putFile, fileName)
        t.close()
        sftp.close()

    def sshDownload(self, inFile, fileName):
        t = paramiko.Transport((self.host, self.port))

        t.connect(username=self.settingInfo['username'],
                  password=str(
                      self.settingInfo['password']))  # 连接方式也可以用key，这里只需要将password=password改为pkey=key，其余的key代码与前面的一样

        sftp = paramiko.SFTPClient.from_transport(t)  # 使用t的设置方式连接远程主机
        sftp.get(inFile, fileName)
        t.close()
        sftp.close()

    @abstractmethod
    def beforeExeCmd(self):
        return

    @abstractmethod
    def afterExeCmd(self):
        return

    def __exeCmd(self):
        """非严格模式执行命令"""
        s = self.getConnect()
        for index, cmd in enumerate(self.settingInfo['cmd']):
            key = cmd.keys()[0]
            print(key)
            stdin, stdout, stderr = s.exec_command(key)
        s.close()

    def __strictExeCmd(self):
        """ 严格模式执行命令，即验证stdout，不符合预期将抛出错误中断线程,外面到线程要接收错误，并退出线程。"""
        s = self.getConnect()
        for index, cmd in enumerate(self.settingInfo['cmd']):
            stdin, stdout, stderr = s.exec_command(cmd[index].keys()[0])
            if stdout.read() != cmd[cmd[index].keys()[0]]:
                raise RemoteException.stractValException(RemoteException(), index, cmd, stdout)
        s.close()

    def __upFile(self, fileName, filePathName):
        self.sshUpload(fileName, filePathName)
        s = self.getConnect()
        s.exec_command('chmod 777 ' + filePathName)
        s.close()

    def strictUpFile(self):

        return

    def upRun(self, fileName, filePathName):
        self.beforeExeCmd()
        self.__upFile(fileName, filePathName)
        self.afterExeCmd()

    def strictUpRun(self):
        self.beforeExeCmd()

        self.afterExeCmd()

    def runSSHCmd(self):
        """ 执行命令"""
        self.beforeExeCmd()
        self.__exeCmd()
        self.afterExeCmd()

    def strictRunSShCmd(self):
        """ 严格执行命令，外层接收错误"""
        self.beforeExeCmd()
        self.__strictExeCmd()
        self.afterExeCmd()
