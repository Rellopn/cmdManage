# -*- coding: utf-8 -*-
from src.AbsSSHConnect import AbsSSHConnect


class RedisClusterSSHConnect(AbsSSHConnect):
    """
        实现了 抽象类的两个抽象方法。此类是被线程所调用的执行方法
        :param settingInfo @see AbsSSHConnect
        :param setting 配置文件 -- 这个是自定义的，这里的主要目的是把setting文件传到服务器上。
                                  这里是RedisCluster的配置
    """

    def __init__(self, settingInfo, setting):
        AbsSSHConnect.__init__(self, settingInfo, setting)

    def beforeExeCmd(self):
        print("\033[1;31;40m正在处理的id：" + str(self.settingInfo['id'])+"请耐心等待下\033[0m")
        settingInfo = self.settingInfo
        s = self.getConnect()
        # 进入workdir目录下，新建端口号的文件夹，然后把设置的文件上传上去
        s.exec_command('cd ' + settingInfo['workDir'])
        s.exec_command('mkdir redis_cluster')
        for port in settingInfo['redisPort']:
            port = str(port)
            s.exec_command('cd redis_cluster && mkdir ' + port)
            addStr = '''
port %s
logfile "/root/redis_cluster/%s/%s.log"
cluster-config-file %s/redis_cluster/%s/nodes-%s.conf
''' % (port, port, port, settingInfo['workDir'], port, port)
            thisConf = addStr + self.setting
            # 生成redis启动的配置文件，端口号+id保证唯一性
            f = open(port + str(self.settingInfo['id']) + '.conf', 'w')
            f.write(thisConf)
            f.close()
            self.sshUpload(port + str(self.settingInfo['id']) + '.conf',
                           settingInfo['workDir'] + '/redis_cluster/' + port + '/' + port + '.conf')
        s.close()
        return

    def afterExeCmd(self):
        s = self.getConnect()
        i, o, e = s.exec_command(
            'cd ' + self.settingInfo['workDir'] + ' && ./redisCluster' + str(self.settingInfo['id']) + '.sh')
        o.read()
        s.close()
        print('线程结束：' + str(self.settingInfo['id']))
        return
