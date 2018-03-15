# -*- coding: utf-8 -*-

from AbsCallBack import AbsCallBack
import os

import RedisClusterSSHConnect


class RedisClusterCallBack(AbsCallBack):
    """
        默认的回调类 功能说明建见 AbsCallBacks
    """

    def __init__(self, config):
        """ 初始化的时候传入配置参数"""
        AbsCallBack.__init__(self, config)

    def beforeInit(self):
        print('call callback function:beforeInit()')
        return

    def beforeReadyTiExeSh(self):
        print('call callback function:beforeReadyTiExeSh()')
        return

    def beforeExeSh(self):
        print('call callback function:beforeExeSh()')
        return

    def afterExeSh(self):
        print('call callback function:afterExeSh()')
        print('clear generate files')
        for oneServer in self.config.loadDic['settingYaml']['settingInfo']:
            for port in oneServer['redisPort']:
                os.remove(str(port)+str(oneServer['id']) + '.conf')
            os.remove('redisCluster' + str(oneServer['id']) + '.sh')
        print('clear done')
        print('strat run build cluster commend')
        allSettingInfo = self.config.loadDic['settingYaml']['settingInfo']
        connectInfo = self.config.loadDic['settingYaml']['settingInfo'][0]
        customerSetting = self.config.generateCustSetting

        # 拼出来 IP、端口
        slave = self.config.loadDic['settingYaml']['clusterInfo'][0]['slave']
        info = ''
        for everyOne in allSettingInfo:
            for one in everyOne['redisPort']:
                info += ' ' + str(everyOne['ip']) + ':' + str(one)
        noslave = info
        info = str(slave) + info

        innerStr = """#!/bin/bash
yum install -y gem
gem install redis
if [ $? -eq 0 ]
then
    echo ''
else
    echo ''
    curl -L get.rvm.io | bash -s stable 
    if [ $? -eq 0 ]
    then
        echo 'rvm'
        pwd
    else
        echo 'rvm'
        curl -sSL https://rvm.io/mpapis.asc | gpg2 --import -
        curl -L get.rvm.io | bash -s stable
    fi
    rvmSh=`find / -name rvm.sh`
    source $rvmSh
    rvm install 2.2.2
    rvm use 2.2.2
    gem install redis
fi
# cd /usr/local/redis/bin && ./redis-trib.rb  create --replicas""" 
        f = open('redisPerpaerCluster.sh', 'w')
        f.write(innerStr)
        f.close()

        rcsc = RedisClusterSSHConnect.RedisClusterSSHConnect(connectInfo, customerSetting)
        rcsc.sshUpload('redisPerpaerCluster.sh', connectInfo['workDir'] + '/redisPerpaerCluster.sh')
        # 如果是windows平台，需要转换编码
        execmd = 'cd ' + connectInfo[
            'workDir'] + ' && chmod 777 redisPerpaerCluster.sh && dos2unix redisPerpaerCluster.sh && ./redisPerpaerCluster.sh'

        execmd2 = 'cd /usr/local/redis/bin && ./redis-trib.rb  create --replicas %s' % info
        if slave == 0:
            execmd2 = 'cd /usr/local/redis/bin && ./redis-trib.rb  create %s' % noslave
        i, o, e = rcsc.getConnect().exec_command(execmd)
        print("maby the next step speed long time,if across 10 minuite,retry.")
        print("remote check ruby version")
        print(o.read())
        print("ruby installed")
        i, o, e = rcsc.getConnect().exec_command(execmd2)
        i.write('yes\n')
        i.flush()
        print(o.read())
        os.remove('redisPerpaerCluster.sh')
        print('complate,enjoy it!')
