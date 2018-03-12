# -*- coding: utf-8 -*-
import time

import AbsCallBack
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
        print('回调函数调用:beforeInit()')
        return

    def beforeReadyTiExeSh(self):
        print('回调函数调用:beforeReadyTiExeSh()')
        return

    def beforeExeSh(self):
        print('回调函数调用:beforeExeSh()')
        return

    def afterExeSh(self):
        print('回调函数调用:afterExeSh()')
        print('清除生成的文件')
        for oneServer in self.config.loadDic['settingYaml']['settingInfo']:
            for port in oneServer['redisPort']:
                os.remove(str(port) + '.conf')
            os.remove('redisCluster' + str(oneServer['id']) + '.sh')
        print('清除完成')
        print('开始运行集群 命令')
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

        innerStr = """
        #!/bin/bash
        yum install gem -y
        gem install redis
        if [ $? -eq 0 ]
        then
            echo 'gem install 成功 '
        else
            echo 'gem install 失败 '
            curl -L get.rvm.io | bash -s stable 
            if [ $? -eq 0 ]
            then
                echo 'rvm 成功 '
                pwd
            else
                echo 'rvm 失败 '
                curl -sSL https://rvm.io/mpapis.asc | gpg2 --import -
                curl -L get.rvm.io | bash -s stable
            fi
            rvmSh=`find / -name rvm.sh`
            source $rvmSh
            rvm install 2.2.2
            rvm use 2.2.2
            gem install redis
        fi
         # cd /usr/local/redis/bin && ./redis-trib.rb  create --replicas %s
                """ % info
        f = open('redisPerpaerCluster.sh', 'w')
        f.write(innerStr)
        f.close()

        rcsc = RedisClusterSSHConnect(connectInfo, customerSetting)
        rcsc.sshUpload('redisPerpaerCluster.sh', connectInfo['workDir'] + '/redisPerpaerCluster.sh')
        time.sleep(1)
        execmd = 'cd ' + connectInfo[
            'workDir'] + ' && chmod 777 redisPerpaerCluster.sh && ./redisPerpaerCluster.sh'

        execmd2 = 'cd /usr/local/redis/bin && ./redis-trib.rb  create --replicas %s' % info
        if slave == 0:
            execmd2 = 'cd /usr/local/redis/bin && ./redis-trib.rb  create %s' % info
        i, o, e = rcsc.getConnect().exec_command(execmd)
        o.read()
        i, o, e = rcsc.getConnect().exec_command(execmd2)
        i.write('yes\n')
        i.flush()
        o.read()
        os.remove('redisPerpaerCluster.sh')
        print('完成')
