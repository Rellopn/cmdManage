# -*- coding: utf-8 -*-
class RedisClusterCmdFactory():
    """
        生成命令的场，根据参数工厂生成的参数，在此组装成线程执行的命令。

        :param param 从参数工厂生成的settingInfo

        :param setting 配置文件
    """

    def __init__(self, param, setting, bootSetting):
        self.param = param
        self.setting = setting
        self.bootSetting = bootSetting

    # 返回的格式 ：[
    #            {setting:xxxxYaml}
    #            {port:[7001,7002]}
    #            {slave:1}
    #            {username: root}
    #            {password: asd6614250}
    #            {ip: 192.168.1.157}
    #            {sshPort: 22}
    #            {workDir:'/root'}
    #            {cmd:[
    #                  {ls:'0'}
    #                  {pwd:'/root'}
    #                   ]}
    #             ]
    def getYumRedisClusterCmd(self):
        """ 生成redisCluster的命令 """
        tempParams = self.param
        # 循环传入的 settingInfo,为每一个配置添加
        for index, oneServe in enumerate(self.param):
            # 命令集合
            cmd = []
            # 首先进入工作目录
            cmd.append({'cd ' + oneServe['workDir']: '0'})
            # yum 安装必要的包
            cmd.append({'yum install ' + self.bootSetting['necessaryPackage'] + ' -y': '0'})
            # 创建一个下载源码的目录并且进入
            cmd.append({'mkdir redis_source': '0'})
            cmd.append({'cd redis_source': '0'})
            # 下载redis 包,从bootstrap下获取
            cmd.append({'wget -c ' + self.bootSetting['redisAddress'] + ' -O redis.tar.gz': '0'})
            # 解压缩
            cmd.append({'tar -zxvf redis.tar.gz': '0'})
            cmd.append({'find ./ -name redis-*': './redis-3.2.8'})
            # 进入 make
            cmd.append({'cd redis-3.2.8 && make': '0'})
            # 进入src 设置安装目录
            cmd.append({'cd src && make install PREFIX=/usr/local/redis': '0'})
            # 拷贝reids集群文件和config文件
            cmd.append({'cp /root/redis_source/redis-3.2.8/src/redis-trib.rb /usr/local/redis/bin ': '0'})
            cmd.append({'cp /root/redis_source/redis-3.2.8/redis.conf /usr/local/redis/bin/': '0'})
            # # 创建cluster文件夹
            # cmd.append({'cd ' + oneServe['workDir'] + ' && mkdir redis-cluster && cd redis-cluster': '0'})
            # 为每个 port 建立文件夹和单独config文件 在本地生成并上传
            # for index, port in enumerate(oneServe['port']):
            #     cmd.append({'mkdir ' + port + ' && cd ' + oneServe['workDir'], '0'})
            # 后台启动 每个 redis带有集群配置的实例
            cmd.append({'cd /usr/local/redis/bin': '0'})
            for port in oneServe['redisPort']:
                cmd.append({'./redis-server ' + oneServe['workDir'] + '/redis_cluster/' + str(port) + '/' + str(
                    port) + '.conf &': '0'})

            f = open('redisCluster' + str(oneServe['id']) + '.sh', 'w')
            f.write('#!/bin/bash \n')
            for c in cmd:
                f.write(c.keys()[0] + '\n')
            f.write('rm -- "$0"')
            f.close()
            tempParams[index]['cmd'] = cmd
        self.param = tempParams
